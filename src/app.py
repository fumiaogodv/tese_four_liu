"""应用程序主循环：单一入口，整合菜单导航与各功能模块。"""

from __future__ import annotations

from src.exceptions import OralCalcError
from src.handlers import HANDLERS
from src.interactive import run_interactive_practice
from src.io.console import ConsoleIO, TextIO
from src.menu import MenuNavigator, MenuState


class Application:
    """口算练习系统应用：程序集成 + CLI 菜单界面。"""

    def __init__(self, io: TextIO | None = None) -> None:
        self.io = io or ConsoleIO()
        self.navigator = MenuNavigator(self.io)

    def run(self) -> None:
        """主循环：显示菜单 → 数字选择 → 执行 → 返回菜单，直至退出。"""
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
        if handler_name == "interactive_practice":
            try:
                run_interactive_practice(self.io)
            except OralCalcError as e:
                self.io.println(f"\n错误: {e}")
            except KeyboardInterrupt:
                self.io.println("\n已取消。")
            return

        handler = HANDLERS.get(handler_name)
        if not handler:
            self.io.println("功能未实现。")
            return
        try:
            handler(self.io)
        except OralCalcError as e:
            self.io.println(f"\n错误: {e}")
        except KeyboardInterrupt:
            self.io.println("\n已取消。")


def run(io: TextIO | None = None) -> None:
    Application(io).run()
