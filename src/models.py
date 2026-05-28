"""数据建模：练习项、练习卷、判题结果、汇总统计。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from src.contracts import invariant, require


@dataclass
class ExerciseItem:
    """单道题：算式 + 标准答案。"""

    seq: int
    expression: str
    correct_answer: int

    def __post_init__(self) -> None:
        require(self.seq >= 1, "题号从1开始")
        invariant(bool(self.expression), "算式不能为空")


@dataclass
class PracticeSession:
    """一次练习卷：含 session_id、类型、题目列表。"""

    session_id: str
    practice_date: str  # YYYY-MM-DD
    practice_type: str  # addition | subtraction | mixed
    exercises: list[ExerciseItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        require(bool(self.session_id), "session_id 必填")
        invariant(len(self.exercises) > 0, "练习卷至少包含一题")

    @property
    def total(self) -> int:
        return len(self.exercises)


@dataclass
class StudentAnswer:
    seq: int
    expression: str
    student_answer: int


@dataclass
class GradeDetail:
    seq: int
    expression: str
    correct_answer: int
    student_answer: int
    is_correct: bool


@dataclass
class GradeResult:
    """判题结果：可序列化到 CSV。"""

    session_id: str
    practice_date: str
    practice_type: str
    total: int
    correct: int
    details: list[GradeDetail] = field(default_factory=list)

    @property
    def score(self) -> float:
        if self.total == 0:
            return 0.0
        return round(100.0 * self.correct / self.total, 1)

    @property
    def wrong_expressions(self) -> list[str]:
        return [d.expression for d in self.details if not d.is_correct]

    def __post_init__(self) -> None:
        invariant(self.correct <= self.total, "正确数不能超过总题数")


@dataclass
class WrongStat:
    """错题统计项（聚合数据结构）。"""

    expression: str
    wrong_count: int
    last_session_id: str
