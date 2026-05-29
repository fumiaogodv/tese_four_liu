"""交互式练习单元测试。"""

from src.generator import generate_practice
from src.grader import grade
from src.interactive import collect_answers
from src.models import StudentAnswer


class FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = list(inputs)
        self.lines: list[str] = []

    def prompt(self, message: str, default: str = "") -> str:
        if self._inputs:
            return self._inputs.pop(0)
        return default

    def println(self, message: str = "") -> None:
        self.lines.append(message)


def test_collect_answers_all_correct():
    session = generate_practice("addition", count=3, seed=11)
    answers_str = [str(ex.correct_answer) for ex in session.exercises]
    io = FakeIO(answers_str)
    answers = collect_answers(session, io)
    assert len(answers) == 3
    result = grade(session, answers)
    assert result.score == 100.0


def test_collect_answers_with_wrong():
    session = generate_practice("subtraction", count=2, seed=5)
    ex0 = session.exercises[0]
    io = FakeIO([str(ex0.correct_answer + 1), str(session.exercises[1].correct_answer)])
    answers = collect_answers(session, io)
    result = grade(session, answers)
    assert result.correct == 1
    assert ex0.expression in result.wrong_expressions
