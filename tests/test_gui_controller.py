"""GUI 控制器单元测试（不启动 tkinter）。"""

from pathlib import Path

from src.container import ServiceContainer
from src.gui.controller import GuiController
from src.gui.events import AppEventBus, AppEventType
from src.models import StudentAnswer


class EventCollector:
    def __init__(self) -> None:
        self.events: list = []

    def on_event(self, event) -> None:
        self.events.append(event)


def test_create_practice_notifies_observers(tmp_path):
    bus = AppEventBus()
    collector = EventCollector()
    bus.subscribe(collector)
    ctrl = GuiController(ServiceContainer(tmp_path), bus)
    session = ctrl.create_practice("addition")
    assert session.total == 50
    types = [e.type for e in collector.events]
    assert AppEventType.PRACTICE_CREATED in types
    assert AppEventType.SESSION_LIST_CHANGED in types


def test_interactive_flow_complete(tmp_path):
    ctrl = GuiController(ServiceContainer(tmp_path))
    practice = ctrl.interactive_start_new("addition", count=3)
    assert practice.total == 3
    answers = [ex.correct_answer for ex in practice.exercises]
    result = None
    for ans in answers:
        r = ctrl.interactive_submit_answer(str(ans))
        if r.is_complete:
            result = r.grade_result
    assert result is not None
    assert result.score == 100.0
    assert len(ctrl.list_sessions()) == 1


def test_interactive_rejects_non_integer(tmp_path):
    ctrl = GuiController(ServiceContainer(tmp_path))
    ctrl.interactive_start_new("addition", count=2)
    r = ctrl.interactive_submit_answer("abc")
    assert not r.accepted
    assert not r.is_complete


def test_import_and_grade_via_controller(tmp_path):
    ctrl = GuiController(ServiceContainer(tmp_path))
    session = ctrl.create_practice("subtraction")
    lines = [f"{ex.expression}={ex.correct_answer}" for ex in session.exercises]
    f = tmp_path / "ans.txt"
    f.write_text("\n".join(lines), encoding="utf-8")
    result = ctrl.import_and_grade(session.session_id, f)
    assert result.score == 100.0


def test_get_analyze_text(tmp_path):
    ctrl = GuiController(ServiceContainer(tmp_path))
    text = ctrl.get_analyze_text()
    assert "练习成绩" in text or "暂无" in text
