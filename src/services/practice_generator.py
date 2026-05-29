"""练习卷生成服务（重构后：类封装 + 依赖注入仓储）。"""

from __future__ import annotations

import random
from datetime import date

from src.constants import GENERATION_RULES, PRACTICE_TYPE_LABELS, PRACTICE_TYPE_NAMES
from src.contracts import ensure, require
from src.exceptions import ValidationError
from src.models import ExerciseItem, PracticeSession
from src.parsers import format_expression
from src.repositories.csv_practice_repository import CsvPracticeRepository
from src.services.session_id import SessionIdBuilder


class PracticeGeneratorService:
    def __init__(
        self,
        repository: CsvPracticeRepository,
        session_id_builder: SessionIdBuilder | None = None,
    ) -> None:
        self._repository = repository
        self._session_ids = session_id_builder or SessionIdBuilder()

    def generate(
        self,
        practice_type: str,
        *,
        count: int | None = None,
        seed: int | None = None,
    ) -> PracticeSession:
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
        session_id = self._session_ids.build(
            practice_type,
            today,
            set(self._repository.list_session_ids()),
        )
        session = PracticeSession(
            session_id=session_id,
            practice_date=today.isoformat(),
            practice_type=practice_type,
            exercises=exercises,
        )
        ensure(session.total == n, "题量与要求一致")
        return session

    @staticmethod
    def practice_type_from_choice(choice: str) -> str:
        key = PRACTICE_TYPE_LABELS.get(choice.strip())
        if not key:
            raise ValidationError("请选择 1=加法 2=减法 3=混合")
        return key

    @staticmethod
    def display_type_name(practice_type: str) -> str:
        return PRACTICE_TYPE_NAMES.get(practice_type, practice_type)


def _random_add() -> tuple[str, int]:
    a = random.randint(0, 99)
    b = random.randint(0, 99 - a)
    return format_expression(a, "+", b), a + b


def _random_sub() -> tuple[str, int]:
    a = random.randint(1, 99)
    b = random.randint(0, a)
    return format_expression(a, "-", b), a - b


_GENERATORS = {
    "addition": lambda: _random_add(),
    "subtraction": lambda: _random_sub(),
    "mixed": lambda: _random_add() if random.random() < 0.5 else _random_sub(),
}
