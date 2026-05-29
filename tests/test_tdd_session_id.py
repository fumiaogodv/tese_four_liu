"""SessionIdBuilder TDD 示例测试（红-绿-重构）。"""

from datetime import date

from src.services.session_id import SessionIdBuilder


def test_session_id_first_of_day():
    builder = SessionIdBuilder()
    sid = builder.build("addition", date(2026, 5, 28), set())
    assert sid == "20260528_add"


def test_session_id_avoids_collision():
    builder = SessionIdBuilder()
    existing = {"20260528_add"}
    sid = builder.build("addition", date(2026, 5, 28), existing)
    assert sid == "20260528_add_2"


def test_session_id_increments_suffix():
    builder = SessionIdBuilder()
    existing = {"20260528_add", "20260528_add_2"}
    sid = builder.build("addition", date(2026, 5, 28), existing)
    assert sid == "20260528_add_3"
