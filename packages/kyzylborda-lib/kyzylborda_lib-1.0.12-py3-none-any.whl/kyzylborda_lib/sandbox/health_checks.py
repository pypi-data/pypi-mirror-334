from __future__ import annotations

import abc
import asyncio
from email.message import Message
import os
from typing import TYPE_CHECKING

from ..server.address import parse_uri_address
from .readiness import watch_file_creation
from ..server import tcp

if TYPE_CHECKING:
    from .box import Box


__all__ = ("HealthCheck", "ConnectHealthCheck", "ExistsHealthCheck", "RequestHealthCheck", "parse_health_checks")


async def await_connect_allowed(address: str):
    if address.startswith("unix:"):
        path = address[5:]
        if not os.path.exists(os.path.dirname(path)):
            raise RuntimeError("The directory containing the healthchecked file does not exist")
        await watch_file_creation(path)


class HealthCheck(abc.ABC):
    @abc.abstractmethod
    async def wait(self, box: Box):
        ...


class ConnectHealthCheck(HealthCheck):
    def __init__(self, address: str):
        super().__init__()
        self.address = address


    async def wait(self, box: Box):
        address = box.get_external_socket_address(self.address)
        await await_connect_allowed(address)

        sleep_interval = 0.1
        while True:
            try:
                (await tcp.connect(address)).close()
                break
            except (ConnectionRefusedError, FileNotFoundError):
                await asyncio.sleep(sleep_interval)
                sleep_interval = min(sleep_interval * 2, 3)


class ExistsHealthCheck(HealthCheck):
    def __init__(self, path: str):
        super().__init__()
        self.path = path


    async def wait(self, box: Box):
        await watch_file_creation(box.get_external_file_path(self.path))


class RequestHealthCheck(HealthCheck):
    def __init__(self, uri: str):
        super().__init__()
        self.uri = uri


    async def wait(self, box: Box):
        # Workaround cyclic imports
        from ..server import http

        if self.uri.startswith("http://"):
            uri = self.uri[7:]
        else:
            raise ValueError(f"Unknown URI {self.uri}")

        hostname, pathname = parse_uri_address(uri)

        address = box.get_external_socket_address(hostname)
        await await_connect_allowed(address)

        header = http.RequestHeader(b"")
        header.method = "GET"
        header.path = pathname
        header.headers = Message()
        header.headers["Host"] = "localhost" if hostname.startswith("unix:") else hostname
        header.headers["Connection"] = "close"
        request = http.Request(header, b"")

        sleep_interval = 0.1
        while True:
            try:
                res = await http.request(request, address)
                res.data.close()
                if res.status_code < 400:
                    break
            except (ConnectionRefusedError, FileNotFoundError):
                pass
            await asyncio.sleep(sleep_interval)
            sleep_interval = min(sleep_interval * 2, 3)


def parse_health_checks(data: dict[str, str]) -> list[HealthCheck]:
    result: list[HealthCheck] = []
    for kind, value in data.items():
        if kind == "connect":
            result.append(ConnectHealthCheck(value))
        elif kind == "exists":
            result.append(ExistsHealthCheck(value))
        elif kind == "request":
            result.append(RequestHealthCheck(value))
        else:
            raise ValueError(f"Unknown healthcheck {kind}")
    return result
