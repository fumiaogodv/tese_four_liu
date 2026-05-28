"""契约式编程：前置/后置条件与不变量检查。"""

from __future__ import annotations

from typing import TypeVar

from src.exceptions import ValidationError

T = TypeVar("T")


def require(condition: bool, message: str) -> None:
    """前置条件：不满足则拒绝继续。"""
    if not condition:
        raise ValidationError(message)


def ensure(condition: bool, message: str) -> None:
    """后置条件：操作完成后必须成立。"""
    if not condition:
        raise ValidationError(f"后置条件违反: {message}")


def invariant(condition: bool, message: str) -> None:
    """不变量：对象应始终满足的性质。"""
    if not condition:
        raise ValidationError(f"不变量违反: {message}")
