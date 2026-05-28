from pathlib import Path

import pytest

from src.generator import generate_practice
from src.grader import grade, parse_answers_from_file
from src.models import StudentAnswer


def test_grade_all_correct(tmp_path):
    session = generate_practice("addition", count=5, seed=99)
    answers = [
        StudentAnswer(seq=ex.seq, expression=ex.expression, student_answer=ex.correct_answer)
        for ex in session.exercises
    ]
    result = grade(session, answers)
    assert result.correct == 5
    assert result.score == 100.0


def test_grade_with_wrong(tmp_path):
    session = generate_practice("subtraction", count=3, seed=7)
    ex0 = session.exercises[0]
    answers = [
        StudentAnswer(seq=ex.seq, expression=ex.expression, student_answer=ex.correct_answer)
        for ex in session.exercises
    ]
    answers[0] = StudentAnswer(
        seq=ex0.seq, expression=ex0.expression, student_answer=ex0.correct_answer + 1
    )
    result = grade(session, answers)
    assert result.correct == 2
    assert ex0.expression in result.wrong_expressions


def test_parse_answers_from_file(tmp_path):
    session = generate_practice("addition", count=3, seed=3)
    lines = [f"{ex.expression}={ex.correct_answer}" for ex in session.exercises]
    f = tmp_path / "ans.txt"
    f.write_text("\n".join(lines), encoding="utf-8")
    parsed = parse_answers_from_file(f, session)
    assert len(parsed) == 3
