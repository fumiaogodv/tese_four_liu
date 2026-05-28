"""CSV 持久化：练习卷、答案、成绩、错题统计。"""

from __future__ import annotations

import csv
from pathlib import Path

from src.constants import (
    CSV_ANSWER_HEADERS,
    CSV_PRACTICE_HEADERS,
    CSV_RESULT_HEADERS,
    CSV_WRONG_STAT_HEADERS,
)
from src.contracts import ensure, require
from src.exceptions import NotFoundError, StorageError, ValidationError
from src.models import ExerciseItem, GradeResult, PracticeSession, StudentAnswer, WrongStat
from src.parsers import normalize_session_id, parse_expression

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _path(name: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / name


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except OSError as e:
        raise StorageError(f"读取失败 {path}: {e}") from e
    except csv.Error as e:
        raise StorageError(f"CSV 格式错误 {path}: {e}") from e


def _write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    try:
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    except OSError as e:
        raise StorageError(f"写入失败 {path}: {e}") from e


def save_practice(session: PracticeSession) -> Path:
    path = _path("practices.csv")
    existing = [r for r in _read_csv(path) if r.get("session_id") != session.session_id]
    new_rows = []
    for ex in session.exercises:
        new_rows.append(
            {
                "session_id": session.session_id,
                "date": session.practice_date,
                "practice_type": session.practice_type,
                "seq": str(ex.seq),
                "expression": ex.expression,
                "correct_answer": str(ex.correct_answer),
            }
        )
    _write_csv(path, CSV_PRACTICE_HEADERS, existing + new_rows)
    ensure(path.exists(), "练习文件应已创建")
    return path


def load_practice(session_id: str) -> PracticeSession:
    session_id = normalize_session_id(session_id)
    rows = [r for r in _read_csv(_path("practices.csv")) if r.get("session_id") == session_id]
    if not rows:
        raise NotFoundError(f"未找到练习卷: {session_id}")

    rows.sort(key=lambda r: int(r["seq"]))
    exercises = [
        ExerciseItem(
            seq=int(r["seq"]),
            expression=r["expression"],
            correct_answer=int(r["correct_answer"]),
        )
        for r in rows
    ]
    first = rows[0]
    return PracticeSession(
        session_id=session_id,
        practice_date=first["date"],
        practice_type=first["practice_type"],
        exercises=exercises,
    )


def list_session_ids() -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for r in _read_csv(_path("practices.csv")):
        sid = r.get("session_id", "")
        if sid and sid not in seen:
            seen.add(sid)
            ids.append(sid)
    return sorted(ids, reverse=True)


def save_answers(session_id: str, answers: list[StudentAnswer]) -> Path:
    session_id = normalize_session_id(session_id)
    path = _path("answers.csv")
    existing = [r for r in _read_csv(path) if r.get("session_id") != session_id]
    rows = [
        {
            "session_id": session_id,
            "seq": str(a.seq),
            "expression": a.expression,
            "student_answer": str(a.student_answer),
        }
        for a in answers
    ]
    _write_csv(path, CSV_ANSWER_HEADERS, existing + rows)
    return path


def load_answers(session_id: str) -> list[StudentAnswer]:
    session_id = normalize_session_id(session_id)
    rows = [r for r in _read_csv(_path("answers.csv")) if r.get("session_id") == session_id]
    if not rows:
        raise NotFoundError(f"未找到答案: {session_id}")
    rows.sort(key=lambda r: int(r["seq"]))
    return [
        StudentAnswer(
            seq=int(r["seq"]),
            expression=r["expression"],
            student_answer=int(r["student_answer"]),
        )
        for r in rows
    ]


def save_grade_result(result: GradeResult) -> Path:
    path = _path("results.csv")
    existing = [r for r in _read_csv(path) if r.get("session_id") != result.session_id]
    wrong = ";".join(result.wrong_expressions)
    row = {
        "session_id": result.session_id,
        "date": result.practice_date,
        "practice_type": result.practice_type,
        "total": str(result.total),
        "correct": str(result.correct),
        "score": str(result.score),
        "wrong_expressions": wrong,
    }
    _write_csv(path, CSV_RESULT_HEADERS, existing + [row])
    _update_wrong_stats(result)
    return path


def load_all_results() -> list[GradeResult]:
    results: list[GradeResult] = []
    for r in _read_csv(_path("results.csv")):
        try:
            results.append(
                GradeResult(
                    session_id=r["session_id"],
                    practice_date=r["date"],
                    practice_type=r["practice_type"],
                    total=int(r["total"]),
                    correct=int(r["correct"]),
                    details=[],
                )
            )
        except (KeyError, ValueError) as e:
            raise StorageError(f"成绩记录损坏: {e}") from e
    return results


def _update_wrong_stats(result: GradeResult) -> None:
    path = _path("wrong_stats.csv")
    stats: dict[str, WrongStat] = {}
    for r in _read_csv(path):
        stats[r["expression"]] = WrongStat(
            expression=r["expression"],
            wrong_count=int(r["wrong_count"]),
            last_session_id=r["last_session_id"],
        )
    for expr in result.wrong_expressions:
        if expr in stats:
            stats[expr] = WrongStat(
                expr, stats[expr].wrong_count + 1, result.session_id
            )
        else:
            stats[expr] = WrongStat(expr, 1, result.session_id)
    rows = [
        {
            "expression": s.expression,
            "wrong_count": str(s.wrong_count),
            "last_session_id": s.last_session_id,
        }
        for s in sorted(stats.values(), key=lambda x: (-x.wrong_count, x.expression))
    ]
    _write_csv(path, CSV_WRONG_STAT_HEADERS, rows)


def load_wrong_stats(min_count: int = 1) -> list[WrongStat]:
    out: list[WrongStat] = []
    for r in _read_csv(_path("wrong_stats.csv")):
        c = int(r["wrong_count"])
        if c >= min_count:
            out.append(
                WrongStat(
                    expression=r["expression"],
                    wrong_count=c,
                    last_session_id=r["last_session_id"],
                )
            )
    return sorted(out, key=lambda x: (-x.wrong_count, x.expression))
