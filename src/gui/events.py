"""GUI 事件与观察者模式。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class AppEventType(str, Enum):
    """应用级事件（观察者模式通知源）。"""

    STATUS = "status"
    PRACTICE_CREATED = "practice_created"
    GRADE_COMPLETED = "grade_completed"
    SESSION_LIST_CHANGED = "session_list_changed"
    INTERACTIVE_STARTED = "interactive_started"
    INTERACTIVE_ANSWERED = "interactive_answered"
    INTERACTIVE_FINISHED = "interactive_finished"
    PANEL_CHANGED = "panel_changed"


@dataclass(frozen=True)
class AppEvent:
    type: AppEventType
    message: str = ""
    data: Any = None


class Observer(Protocol):
    """观察者接口。"""

    def on_event(self, event: AppEvent) -> None: ...


class AppEventBus:
    """主题（Subject）：发布事件，通知所有观察者。"""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers = [o for o in self._observers if o is not observer]

    def notify(self, event: AppEvent) -> None:
        for observer in self._observers:
            observer.on_event(event)
