"""菜单导航单元测试。"""

from io import StringIO

from src.app import Application
from src.constants import main_menu_actions
from src.menu import MenuNavigator, MenuState


class FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = iter(inputs)
        self.lines: list[str] = []

    def prompt(self, message: str, default: str = "") -> str:
        try:
            return next(self._inputs)
        except StopIteration:
            return default

    def println(self, message: str = "") -> None:
        self.lines.append(message)


def test_main_menu_has_six_features_plus_exit():
    actions = main_menu_actions()
    keys = [a.key for a in actions]
    assert keys == ["1", "2", "3", "4", "5", "6", "0"]
    manager = [a for a in actions if a.role == "manager"]
    student = [a for a in actions if a.role == "student"]
    assert len(manager) == 5
    assert len(student) == 1
    assert student[0].handler_name == "interactive_practice"


def test_menu_transition_exit():
    io = FakeIO([])
    nav = MenuNavigator(io)
    state, action = nav.transition("0")
    assert state == MenuState.EXIT
    assert action is None


def test_menu_transition_invalid():
    io = FakeIO([])
    nav = MenuNavigator(io)
    state, action = nav.transition("99")
    assert state == MenuState.MAIN
    assert action is None


def test_application_exit_on_zero():
    io = FakeIO(["0"])
    app = Application(io)
    app.run()
    assert any("再见" in line for line in io.lines)
