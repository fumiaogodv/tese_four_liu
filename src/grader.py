"""grader 兼容层。"""

from __future__ import annotations

from pathlib import Path

from src.container import get_container
from src.models import GradeResult, PracticeSession, StudentAnswer


def grade_session(session_id: str) -> GradeResult:
    return get_container().grader.grade_session(session_id)


def grade(
    practice: PracticeSession,
    answers: list[StudentAnswer],
    *,
    persist: bool = False,
) -> GradeResult:
    return get_container().grader.grade(practice, answers, persist=persist)


def parse_answers_from_file(path: Path, practice: PracticeSession) -> list[StudentAnswer]:
    return get_container().grader.parse_answers_from_file(path, practice)


def import_answers_and_grade(session_id: str, answer_file: Path) -> GradeResult:
    return get_container().grader.import_and_grade(session_id, answer_file)
