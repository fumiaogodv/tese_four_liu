"""export 兼容层。"""

from __future__ import annotations

from pathlib import Path

from src.container import get_container
from src.models import PracticeSession


def export_practice_text(session: PracticeSession, path: Path, *, with_answers: bool = False) -> None:
    get_container().export.export_practice_text(session, path, with_answers=with_answers)
