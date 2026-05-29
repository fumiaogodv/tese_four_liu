"""analyzer 兼容层。"""

from __future__ import annotations

from src.container import get_container
from src.models import GradeResult, WrongStat


def format_results_table(results: list[GradeResult]) -> str:
    return get_container().analyzer.format_results_table(results)


def format_wrong_analysis(stats: list[WrongStat], top_n: int = 15) -> str:
    return get_container().analyzer.format_wrong_analysis(stats, top_n)


def daily_summary(results: list[GradeResult]) -> str:
    return get_container().analyzer.daily_summary(results)


def analyze() -> str:
    return get_container().analyzer.analyze()
