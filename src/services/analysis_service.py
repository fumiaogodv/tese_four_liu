"""数据分析服务（重构后）。"""

from __future__ import annotations

from collections import defaultdict

from src.models import GradeResult, WrongStat
from src.repositories.csv_practice_repository import CsvPracticeRepository
from src.services.practice_generator import PracticeGeneratorService


class AnalysisService:
    def __init__(self, repository: CsvPracticeRepository) -> None:
        self._repository = repository

    def format_results_table(self, results: list[GradeResult]) -> str:
        if not results:
            return "暂无成绩记录。"
        lines = [
            f"{'日期':<12} {'类型':<10} {'session_id':<18} {'得分':>6} {'正确/总':>10}",
            "-" * 62,
        ]
        for r in sorted(results, key=lambda x: (x.practice_date, x.session_id), reverse=True):
            lines.append(
                f"{r.practice_date:<12} "
                f"{PracticeGeneratorService.display_type_name(r.practice_type):<10} "
                f"{r.session_id:<18} {r.score:>6.1f} {r.correct:>4}/{r.total:<4}"
            )
        return "\n".join(lines)

    def format_wrong_analysis(self, stats: list[WrongStat], top_n: int = 15) -> str:
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

    def daily_summary(self, results: list[GradeResult]) -> str:
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

    def analyze(self) -> str:
        results = self._repository.load_all_results()
        stats = self._repository.load_wrong_stats()
        parts = [
            "=== 练习成绩 ===",
            self.format_results_table(results),
            "",
            self.daily_summary(results),
            "",
            "=== 薄弱题目 ===",
            self.format_wrong_analysis(stats),
        ]
        return "\n".join(p for p in parts if p)
