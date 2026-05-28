import pytest

from src.exceptions import ValidationError
from src.parsers import parse_answer_line, parse_expression


def test_parse_expression_add():
    assert parse_expression("48+7") == (48, "+", 7, 55)


def test_parse_expression_sub():
    assert parse_expression("15-6") == (15, "-", 6, 9)


def test_parse_expression_invalid():
    with pytest.raises(ValidationError):
        parse_expression("abc")


def test_parse_expression_add_overflow():
    with pytest.raises(ValidationError):
        parse_expression("60+50")


def test_parse_answer_line():
    expr, ans = parse_answer_line("48+7=55")
    assert expr == "48+7"
    assert ans == 55


def test_parse_answer_line_spaces():
    expr, ans = parse_answer_line(" 48+7 = 55 ")
    assert expr == "48+7"
    assert ans == 55
