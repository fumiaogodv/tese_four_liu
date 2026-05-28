import pytest

from src.generator import generate_practice
from src.grader import grade
from src.models import StudentAnswer
from src.repository import load_practice, load_wrong_stats, save_grade_result, save_practice


@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    monkeypatch.setattr("src.repository.DATA_DIR", tmp_path)
    yield


def test_save_and_load_practice():
    session = generate_practice("addition", count=5, seed=1)
    save_practice(session)
    loaded = load_practice(session.session_id)
    assert loaded.total == 5
    assert loaded.exercises[0].expression == session.exercises[0].expression


def test_wrong_stats_updated():
    session = generate_practice("addition", count=2, seed=2)
    ex = session.exercises[0]
    answers = [
        StudentAnswer(seq=ex.seq, expression=ex.expression, student_answer=0),
        StudentAnswer(
            seq=session.exercises[1].seq,
            expression=session.exercises[1].expression,
            student_answer=session.exercises[1].correct_answer,
        ),
    ]
    result = grade(session, answers)
    save_grade_result(result)
    stats = load_wrong_stats()
    assert any(s.expression == ex.expression for s in stats)
