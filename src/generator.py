"""练习卷生成：表驱动约束，保证不重复算式。"""

from __future__ import annotations

import random
from datetime import date

from src.constants import GENERATION_RULES, PRACTICE_TYPE_LABELS, PRACTICE_TYPE_NAMES
from src.contracts import ensure, require
from src.exceptions import ValidationError
from src.models import ExerciseItem, PracticeSession
from src.parsers import format_expression


def _session_id(practice_type: str, day: date | None = None) -> str:
    """生成唯一 session_id，同日同类型多次练习自动追加序号。"""
    d = day or date.today()
    base = f"{d.strftime('%Y%m%d')}_{practice_type[:3]}"
    try:
        from src.repository import list_session_ids

        existing = set(list_session_ids())
    except OSError:
        existing = set()
    if base not in existing:
        return base
    n = 2
    while f"{base}_{n}" in existing:
        n += 1
    return f"{base}_{n}"


def _random_add() -> tuple[str, int]:
    """加法：和 < 100。"""
    a = random.randint(0, 99)
    b = random.randint(0, 99 - a)
    expr = format_expression(a, "+", b)
    return expr, a + b


def _random_sub() -> tuple[str, int]:
    """减法：差 >= 0。"""
    a = random.randint(1, 99)
    b = random.randint(0, a)
    expr = format_expression(a, "-", b)
    return expr, a - b


_GENERATORS = {
    "addition": lambda: _random_add(),
    "subtraction": lambda: _random_sub(),
    "mixed": lambda: _random_add() if random.random() < 0.5 else _random_sub(),
}


def generate_practice(
    practice_type: str,
    *,
    count: int | None = None,
    seed: int | None = None,
) -> PracticeSession:
    """
    生成一套练习。
    契约：practice_type 合法；生成 count 道不重复算式。
    """
    require(practice_type in _GENERATORS, f"未知练习类型: {practice_type}")
    rules = GENERATION_RULES[practice_type]
    n = count if count is not None else rules["count"]
    require(1 <= n <= 200, "题量应在 1~200 之间")

    if seed is not None:
        random.seed(seed)

    seen: set[str] = set()
    exercises: list[ExerciseItem] = []
    attempts = 0
    max_attempts = n * 500

    while len(exercises) < n and attempts < max_attempts:
        attempts += 1
        expr, ans = _GENERATORS[practice_type]()
        if expr in seen:
            continue
        seen.add(expr)
        exercises.append(
            ExerciseItem(seq=len(exercises) + 1, expression=expr, correct_answer=ans)
        )

    if len(exercises) < n:
        raise ValidationError(f"无法在合理尝试内生成 {n} 道不重复题目")

    today = date.today()
    session = PracticeSession(
        session_id=_session_id(practice_type, today),
        practice_date=today.isoformat(),
        practice_type=practice_type,
        exercises=exercises,
    )
    ensure(session.total == n, "题量与要求一致")
    return session


def practice_type_from_menu_choice(choice: str) -> str:
    key = PRACTICE_TYPE_LABELS.get(choice.strip())
    if not key:
        raise ValidationError("请选择 1=加法 2=减法 3=混合")
    return key


def display_type_name(practice_type: str) -> str:
    return PRACTICE_TYPE_NAMES.get(practice_type, practice_type)
