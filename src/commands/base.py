"""命令模式：菜单功能与业务逻辑解耦。"""

from __future__ import annotations

from typing import Protocol

from src.container import ServiceContainer
from src.io.console import TextIO


class Command(Protocol):
    """可执行菜单命令。"""

    def execute(self, io: TextIO, services: ServiceContainer) -> None: ...
