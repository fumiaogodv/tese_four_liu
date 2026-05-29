"""repository 兼容层：委托给 CsvPracticeRepository。"""

from __future__ import annotations

from pathlib import Path

from src.container import get_container, reset_container
from src.models import GradeResult, PracticeSession, StudentAnswer, WrongStat
from src.paths import get_data_dir

DATA_DIR = get_data_dir()


def _repo():
    return get_container().repository


def save_practice(session: PracticeSession) -> Path:
    return _repo().save_practice(session)


def load_practice(session_id: str) -> PracticeSession:
    return _repo().load_practice(session_id)


def list_session_ids() -> list[str]:
    return _repo().list_session_ids()


def save_answers(session_id: str, answers: list[StudentAnswer]) -> Path:
    return _repo().save_answers(session_id, answers)


def load_answers(session_id: str) -> list[StudentAnswer]:
    return _repo().load_answers(session_id)


def save_grade_result(result: GradeResult) -> Path:
    return _repo().save_grade_result(result)


def load_all_results() -> list[GradeResult]:
    return _repo().load_all_results()


def load_wrong_stats(min_count: int = 1) -> list[WrongStat]:
    return _repo().load_wrong_stats(min_count)


__all__ = [
    "DATA_DIR",
    "save_practice",
    "load_practice",
    "list_session_ids",
    "save_answers",
    "load_answers",
    "save_grade_result",
    "load_all_results",
    "load_wrong_stats",
    "reset_container",
]
