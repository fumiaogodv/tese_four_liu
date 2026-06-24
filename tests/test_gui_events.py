"""观察者模式单元测试。"""

from src.gui.events import AppEvent, AppEventBus, AppEventType


def test_observer_receives_notify():
    bus = AppEventBus()
    received = []

    class O:
        def on_event(self, event):
            received.append(event)

    o = O()
    bus.subscribe(o)
    bus.notify(AppEvent(AppEventType.STATUS, "hello"))
    assert len(received) == 1
    assert received[0].message == "hello"


def test_unsubscribe():
    bus = AppEventBus()
    count = 0

    class O:
        def on_event(self, event):
            nonlocal count
            count += 1

    o = O()
    bus.subscribe(o)
    bus.notify(AppEvent(AppEventType.STATUS, "a"))
    bus.unsubscribe(o)
    bus.notify(AppEvent(AppEventType.STATUS, "b"))
    assert count == 1
