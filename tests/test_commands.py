"""命令模式单元测试。"""

from src.commands.manager_commands import CommandRegistry, CreatePracticeCommand
from src.container import ServiceContainer


class FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = list(inputs)
        self.lines: list[str] = []

    def prompt(self, message: str, default: str = "") -> str:
        if self._inputs:
            return self._inputs.pop(0)
        return default

    def println(self, message: str = "") -> None:
        self.lines.append(message)


def test_create_practice_command(tmp_path):
    services = ServiceContainer(tmp_path)
    io = FakeIO(["1"])
    CreatePracticeCommand().execute(io, services)
    assert services.repository.list_session_ids()
    assert any("已生成" in line for line in io.lines)


def test_command_registry_dispatch(tmp_path):
    services = ServiceContainer(tmp_path)
    registry = CommandRegistry(services)
    io = FakeIO(["1"])
    registry.execute("create_practice", io)
    assert len(services.repository.list_session_ids()) == 1


def test_command_registry_unknown():
    services = ServiceContainer()
    registry = CommandRegistry(services)
    io = FakeIO([])
    registry.execute("nonexistent", io)
    assert any("未实现" in line for line in io.lines)
