"""练习数据分析：成绩趋势、薄弱题目。"""

from __future__ import annotations

from collections import defaultdict

from src.generator import display_type_name
from src.models import GradeResult, WrongStat
from src.repository import load_all_results, load_wrong_stats


def format_results_table(results: list[GradeResult]) -> str:
    if not results:
        return "暂无成绩记录。"
    lines = [
        f"{'日期':<12} {'类型':<10} {'session_id':<18} {'得分':>6} {'正确/总':>10}",
        "-" * 62,
    ]
    for r in sorted(results, key=lambda x: (x.practice_date, x.session_id), reverse=True):
        lines.append(
            f"{r.practice_date:<12} {display_type_name(r.practice_type):<10} "
            f"{r.session_id:<18} {r.score:>6.1f} {r.correct:>4}/{r.total:<4}"
        )
    return "\n".join(lines)


def format_wrong_analysis(stats: list[WrongStat], top_n: int = 15) -> str:
    if not stats:
        return "暂无错题统计（请先完成判题）。"
    lines = [
        f"错题排行（前 {min(top_n, len(stats))} 道，便于安排重点练习）：",
        f"{'算式':<12} {'错误次数':>8} {'最近练习':<18}",
        "-" * 42,
    ]
    for s in stats[:top_n]:
        lines.append(f"{s.expression:<12} {s.wrong_count:>8} {s.last_session_id:<18}")
    return "\n".join(lines)


def daily_summary(results: list[GradeResult]) -> str:
    """按日期汇总平均分。"""
    by_date: dict[str, list[float]] = defaultdict(list)
    for r in results:
        by_date[r.practice_date].append(r.score)
    if not by_date:
        return ""
    lines = ["按日汇总：", "-" * 30]
    for d in sorted(by_date.keys(), reverse=True):
        scores = by_date[d]
        avg = sum(scores) / len(scores)
        lines.append(f"  {d}: 练习 {len(scores)} 次, 平均分 {avg:.1f}")
    return "\n".join(lines)


def analyze() -> str:
    results = load_all_results()
    stats = load_wrong_stats()
    parts = [
        "=== 练习成绩 ===",
        format_results_table(results),
        "",
        daily_summary(results),
        "",
        "=== 薄弱题目 ===",
        format_wrong_analysis(stats),
    ]
    return "\n".join(p for p in parts if p)
