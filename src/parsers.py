"""字符串与正则：解析算式、答案行、校验输入格式。"""

from __future__ import annotations

import re

from src.contracts import require
from src.exceptions import ValidationError

# 算式：48+7 或 88-21（无等号）
EXPRESSION_PATTERN = re.compile(r"^(\d+)([+\-])(\d+)$")
# 答案行：48+7=55 或 48+7= 55（允许空格）
ANSWER_LINE_PATTERN = re.compile(
    r"^(\d+)([+\-])(\d+)=(\s*)(-?\d+)\s*$"
)
# session_id：日期+类型简写，可带序号如 20260528_add_2
SESSION_ID_PATTERN = re.compile(r"^\d{8}_[a-z]+(_\d+)?$")


def parse_expression(expr: str) -> tuple[int, str, int, int]:
    """
    解析算式字符串，返回 (左操作数, 运算符, 右操作数, 正确答案)。
    契约：加法结果 < 100；减法结果 >= 0。
    """
    require(bool(expr and expr.strip()), "算式不能为空")
    text = expr.strip().replace(" ", "")
    m = EXPRESSION_PATTERN.match(text)
    if not m:
        raise ValidationError(f"算式格式无效: {expr!r}，应为如 48+7 或 15-6")

    left, op, right = int(m.group(1)), m.group(2), int(m.group(3))
    if op == "+":
        value = left + right
        require(value < 100, f"加法结果应小于100: {expr}={value}")
    else:
        value = left - right
        require(value >= 0, f"减法结果应不小于0: {expr}={value}")
    return left, op, right, value


def format_expression(left: int, op: str, right: int) -> str:
    return f"{left}{op}{right}"


def parse_answer_line(line: str) -> tuple[str, int]:
    """解析一行答案：48+7=55 -> (expression, student_answer)。"""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        raise ValidationError("空行或注释行")
    m = ANSWER_LINE_PATTERN.match(stripped.replace(" ", ""))
    if not m:
        raise ValidationError(
            f"答案行格式无效: {line!r}，应为如 48+7=55"
        )
    expr = f"{m.group(1)}{m.group(2)}{m.group(3)}"
    answer = int(m.group(5))
    return expr, answer


def normalize_session_id(session_id: str) -> str:
    require(bool(SESSION_ID_PATTERN.match(session_id.strip())), "session_id 格式无效")
    return session_id.strip()
