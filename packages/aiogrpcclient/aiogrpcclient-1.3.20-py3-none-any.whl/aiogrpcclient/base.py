import asyncio
import inspect
import json
import logging
import sys
import typing
from functools import wraps

import grpc
import yaml
from aiokit import AioThing
from grpc import StatusCode
from grpc.aio import secure_channel
from grpc.experimental.aio import insecure_channel
from izihawa_utils.pb_to_json import MessageToDict
from termcolor import colored


def expose(fn=None, with_from_file=False):
    if fn:
        fn._exposable = True
        fn._with_from_file = with_from_file
    else:

        def real_expose(fn):
            return expose(fn=fn, with_from_file=with_from_file)

        return real_expose
    return fn


def from_file(method):
    async def inner(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            data = yaml.safe_load(file_data)
        elif file_path.endswith(".json"):
            data = json.loads(file_data)
        else:
            raise ValueError(
                f"Unknown format for `{file_path}`, only `json`, `yml` or `json` are supported"
            )
        return await method(**data)

    return inner


def format_json(response):
    return json.dumps(
        MessageToDict(
            response, bytes_to_unicode=True, preserving_proto_field_name=True
        ),
        indent=2,
    )


def format_yaml(response):
    return yaml.safe_dump(
        MessageToDict(
            response, bytes_to_unicode=True, preserving_proto_field_name=True
        ),
        default_flow_style=False,
    ).rstrip("\n")


fmt = {
    "json": format_json,
    "yaml": format_yaml,
}


def add_format(fn):
    oldsig = inspect.signature(fn)
    params = list(oldsig.parameters.values())
    for i, param in enumerate(params):
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            break
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            break
    else:
        i = len(params)
    name = "format"
    while name in oldsig.parameters:
        name += "_"
    newparam = inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, default="json")
    params.insert(i, newparam)
    sig = oldsig.replace(parameters=params)

    @wraps(fn)
    async def exposing_wrapper(self, *args, **kwargs):
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()
        format = bound.arguments[name]
        del bound.arguments[name]
        try:
            f = fn(*bound.args, **bound.kwargs)
            if isinstance(f, typing.AsyncGenerator):
                async for el in f:
                    if isinstance(el, str):
                        print(el)
                    else:
                        print(fmt[format](el))
            else:
                result = await f
                print(fmt[format](result))
        except grpc.aio.AioRpcError as e:
            print(
                f"{colored('ERROR', 'red')}: {e.code()} ({e.details()})",
                file=sys.stderr,
            )

    exposing_wrapper.__signature__ = sig
    return exposing_wrapper


class BaseGrpcClient(AioThing):
    stub_clses = {}

    def __init__(
        self,
        endpoint,
        max_attempts: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 30.0,
        backoff_multiplier: float = 2.0,
        retryable_status_codes: tuple[str] = ("CANCELLED", "UNAVAILABLE"),
        keepalive_time_ms: int = 15000,
        keepalive_timeout_ms: int = 30000,
        connection_timeout: float = None,
        max_message_length: int = 1024 * 1024 * 1024,
        compression=None,
        extra_options: list[tuple[str, typing.Any]] | None = None,
    ):
        super().__init__()
        if endpoint is None:
            raise RuntimeError(
                f"`endpoint` must be passed for {self.__class__.__name__} constructor"
            )

        options = [
            ("grpc.dns_min_time_between_resolutions_ms", 1000),
            ("grpc.initial_reconnect_backoff_ms", 1000),
            ("grpc.lb_policy_name", "round_robin"),
            ("grpc.keepalive_time_ms", keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", keepalive_timeout_ms),
            ("grpc.keepalive_without_calls", 1),
            ("grpc.min_reconnect_backoff_ms", 1000),
            ("grpc.max_reconnect_backoff_ms", 5000),
            ("grpc.max_send_message_length", max_message_length),
            ("grpc.max_receive_message_length", max_message_length),
            ("grpc.enable_retries", 1),
            (
                "grpc.service_config",
                json.dumps(
                    {
                        "methodConfig": [
                            {
                                "name": [{}],
                                "retryPolicy": {
                                    "maxAttempts": max_attempts,
                                    "initialBackoff": f"{initial_backoff}s",
                                    "maxBackoff": f"{max_backoff}s",
                                    "backoffMultiplier": backoff_multiplier,
                                    "retryableStatusCodes": retryable_status_codes,
                                },
                                "waitForReady": True,
                            }
                        ]
                    }
                ),
            ),
        ]
        if extra_options is not None:
            options += extra_options

        self.connection_timeout = connection_timeout
        _, port = endpoint.rsplit(":", maxsplit=1)
        match port:
            case "443":
                self.channel = secure_channel(
                    endpoint,
                    grpc.ssl_channel_credentials(),
                    options,
                    compression=compression,
                )
            case _:
                self.channel = insecure_channel(
                    endpoint, options, compression=compression
                )
        self.stubs = {}
        for stub_name, stub_cls in self.stub_clses.items():
            self.stubs[stub_name] = stub_cls(self.channel)

    async def start(self):
        logging.getLogger("debug").debug(
            {
                "action": "start",
                "mode": "aiogrpcclient",
                "client": self.__class__.__name__,
            }
        )
        await asyncio.wait_for(
            self.channel.channel_ready(), timeout=self.connection_timeout
        )

    async def stop(self):
        await self.channel.close()

    def get_interface(self):
        interface = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and getattr(method, "_exposable", False):
                interface[method_name.replace("_", "-")] = add_format(method)
                if getattr(method, "_with_from_file"):
                    interface[method_name.replace("_", "-") + "-from-file"] = (
                        add_format(from_file(method))
                    )
        return interface
