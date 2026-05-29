"""interactive 兼容层。"""

from __future__ import annotations

from src.container import get_container
from src.io.console import TextIO
from src.models import PracticeSession, StudentAnswer
from src.services.interactive_service import InteractivePracticeService


def collect_answers(practice: PracticeSession, io: TextIO) -> list[StudentAnswer]:
    return get_container().interactive.collect_answers(practice, io)


def run_interactive_practice(io: TextIO) -> None:
    get_container().interactive.run(io)
