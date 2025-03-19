from __future__ import annotations

import abc
import base64
from dataclasses import dataclass
from functools import cache
import json
import os
from tempfile import NamedTemporaryFile
from typing import Optional
import yaml

from .health_checks import HealthCheck, parse_health_checks


__all__ = ("Volume", "BoxEnvironment", "get_environment")


@dataclass
class Volume:
    source: str
    target: str
    options: str

    @classmethod
    def parse(cls, s: str) -> "Volume":
        source, target, *rest = s.split(":", 2)
        return cls(source, target, rest[0] if rest else "")

    def is_named_volume(self) -> bool:
        return "/" not in self.source


@dataclass
class BoxEnvironment:
    image_root: str
    app_root: str
    sandbox_user: str
    sandbox_group: str
    size_limit: str
    work_dir: str
    environ: dict[str, str]
    argv: list[str]
    volumes: list[Volume]
    socket: Optional[str]
    health_checks: list[HealthCheck]
    host_name: str
    cpu_rate: float
    max_pids: int


@cache
def get_environment(name: Optional[str]=None) -> BoxEnvironment:
    if name is None:
        box_names = [name[len("IMAGE_CONFIG_"):] for name in os.environ if name.startswith("IMAGE_CONFIG_")]
        if not box_names:
            raise ValueError("No box found. Have you specified it in daemon.exec?")
        elif len(box_names) > 1:
            raise ValueError("Multiple boxes found--please specify the name of the one you are interested in.")
        return get_environment(box_names[0])


    try:
        docker_config = json.loads(os.environ[f"IMAGE_CONFIG_{name}"])
    except KeyError:
        raise ValueError(f"Unknown box {name}. Have you specified it in daemon.exec?") from None

    try:
        with open(f"/apps/{name}/kyzylborda-box.yml") as f:
            box_config = yaml.unsafe_load(f)
    except FileNotFoundError:
        box_config = {}


    user = docker_config[0]["Config"].get("User", "")  # podman doesn't always populate User
    sandbox_user, _, sandbox_group = user.partition(":")

    size_limit = str(box_config.get("tmpfs-size", "10M"))

    work_dir = docker_config[0]["Config"]["WorkingDir"] or "/"  # might be an empty string

    environ: dict[str, str] = {}
    for line in docker_config[0]["Config"]["Env"]:
        key, _, value = line.partition("=")
        assert key is not None  # mypy, wtf?
        environ[key] = value

    argv = (docker_config[0]["Config"].get("Entrypoint") or []) + (docker_config[0]["Config"].get("Cmd") or [])

    volumes = [Volume.parse(volume) for volume in box_config.get("volumes", [])]

    socket = box_config.get("socket")

    health_checks = parse_health_checks(box_config.get("healthcheck", {}))

    host_name = box_config.get("host_name", os.environ.get("TASK_NAME", "box")[:64])

    cpu_rate = box_config.get("cpu_rate", 0.05)

    max_pids = box_config.get("max_pids", 1000)

    with NamedTemporaryFile("w", delete=False) as f:
        os.fchmod(f.fileno(), 0o444)
        volumes.append(Volume(f.name, "/etc/hostname", "ro"))
        f.write(host_name + "\n")

    with NamedTemporaryFile("w", delete=False) as f:
        os.fchmod(f.fileno(), 0o444)
        volumes.append(Volume(f.name, "/etc/hosts", "ro"))
        f.write(f"""127.0.0.1    localhost {host_name}
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
""")

    return BoxEnvironment(
        f"/images/{name}",
        f"/apps/{name}",
        sandbox_user,
        sandbox_group,
        size_limit,
        work_dir,
        environ,
        argv,
        volumes,
        socket,
        health_checks,
        host_name,
        cpu_rate,
        max_pids
    )
