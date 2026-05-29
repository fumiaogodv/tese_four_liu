"""CLI 菜单导航与状态管理。"""

from __future__ import annotations

from enum import Enum

from src.constants import MainMenuAction, main_menu_actions
from src.io.console import TextIO


class MenuState(str, Enum):
    """菜单状态：用于状态转换图与导航控制。"""

    MAIN = "main"
    EXIT = "exit"


class MenuNavigator:
    """主菜单导航：数字选功能，循环直至退出。"""

    def __init__(self, io: TextIO) -> None:
        self.io = io
        self.state = MenuState.MAIN

    def render_main_menu(self) -> None:
        self.io.println("=" * 52)
        self.io.println("  口算练习系统 — 统一入口 (故事1~6 集成)")
        self.io.println("=" * 52)
        self.io.println("  【华经理】1~5   【小明】6")
        self.io.println("-" * 52)
        for action in main_menu_actions():
            role = "华" if action.role == "manager" else ("明" if action.role == "student" else "  ")
            self.io.println(f"  [{action.key}] ({role}) {action.title}")
        self.io.println("-" * 52)

    def read_choice(self) -> str:
        return self.prompt("\n请输入功能编号", "0")

    def prompt(self, message: str, default: str = "") -> str:
        return self.io.prompt(message, default)

    def resolve_action(self, choice: str) -> MainMenuAction | None:
        return next((a for a in main_menu_actions() if a.key == choice), None)

    def transition(self, choice: str) -> tuple[MenuState, MainMenuAction | None]:
        """根据用户输入决定下一状态与待执行动作。"""
        if choice == "0":
            self.state = MenuState.EXIT
            return self.state, None
        action = self.resolve_action(choice)
        if action is None or action.handler_name == "exit":
            self.state = MenuState.MAIN
            return self.state, None
        self.state = MenuState.MAIN
        return self.state, action
