from src.generator import generate_practice


def test_generate_addition_unique_count():
    session = generate_practice("addition", count=20, seed=42)
    assert session.total == 20
    exprs = [e.expression for e in session.exercises]
    assert len(exprs) == len(set(exprs))


def test_generate_mixed_types():
    for ptype in ("addition", "subtraction", "mixed"):
        session = generate_practice(ptype, count=10, seed=1)
        assert session.practice_type == ptype
