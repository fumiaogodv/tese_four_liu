"""应用程序主循环：依赖注入 + 命令模式。"""

from __future__ import annotations

from src.commands.manager_commands import CommandRegistry
from src.container import ServiceContainer, get_container
from src.exceptions import OralCalcError
from src.io.console import ConsoleIO, TextIO
from src.menu import MenuNavigator, MenuState


class Application:
    """口算练习系统应用（重构后）。"""

    def __init__(
        self,
        io: TextIO | None = None,
        services: ServiceContainer | None = None,
    ) -> None:
        self.io = io or ConsoleIO()
        self.services = services or get_container()
        self.navigator = MenuNavigator(self.io)
        self.commands = CommandRegistry(self.services)

    def run(self) -> None:
        while self.navigator.state != MenuState.EXIT:
            self.navigator.render_main_menu()
            choice = self.navigator.read_choice()
            state, action = self.navigator.transition(choice)
            if state == MenuState.EXIT:
                self.io.println("\n感谢使用，再见！")
                break
            if action is None:
                self.io.println("\n无效选项，请输入菜单上的数字编号。")
                continue
            self._dispatch(action.handler_name)

    def _dispatch(self, handler_name: str) -> None:
        try:
            self.commands.execute(handler_name, self.io)
        except OralCalcError as e:
            self.io.println(f"\n错误: {e}")
        except KeyboardInterrupt:
            self.io.println("\n已取消。")


def run(io: TextIO | None = None, services: ServiceContainer | None = None) -> None:
    Application(io, services).run()
