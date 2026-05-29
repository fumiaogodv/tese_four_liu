"""服务层单元测试。"""

from pathlib import Path

from src.container import ServiceContainer
from src.models import StudentAnswer
from src.services.practice_generator import PracticeGeneratorService


def test_service_container_wiring(tmp_path):
    c = ServiceContainer(tmp_path)
    assert c.repository.data_dir == tmp_path
    assert c.generator is not None
    assert c.grader is not None


def test_generator_service_via_container(tmp_path):
    c = ServiceContainer(tmp_path)
    session = c.generator.generate("addition", count=5, seed=1)
    c.repository.save_practice(session)
    loaded = c.repository.load_practice(session.session_id)
    assert loaded.total == 5


def test_grading_service_persists(tmp_path):
    c = ServiceContainer(tmp_path)
    session = c.generator.generate("addition", count=2, seed=2)
    answers = [
        StudentAnswer(
            seq=ex.seq,
            expression=ex.expression,
            student_answer=ex.correct_answer,
        )
        for ex in session.exercises
    ]
    result = c.grader.grade(session, answers, persist=True)
    assert result.score == 100.0
    assert len(c.repository.load_all_results()) == 1


def test_export_service(tmp_path):
    c = ServiceContainer(tmp_path)
    session = c.generator.generate("subtraction", count=5, seed=3)
    out = tmp_path / "out.txt"
    c.export.export_practice_text(session, out)
    text = out.read_text(encoding="utf-8")
    assert "练习卷" in text
    assert session.exercises[0].expression in text
