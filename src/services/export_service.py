"""练习卷导出服务。"""

from __future__ import annotations

from pathlib import Path

from src.models import PracticeSession
from src.services.practice_generator import PracticeGeneratorService


class ExportService:
    def export_practice_text(
        self,
        session: PracticeSession,
        path: Path,
        *,
        with_answers: bool = False,
    ) -> None:
        title = (
            f"【答案卷】{PracticeGeneratorService.display_type_name(session.practice_type)}"
            if with_answers
            else f"【练习卷】{PracticeGeneratorService.display_type_name(session.practice_type)}"
        )
        lines = [
            title,
            f"编号: {session.session_id}  日期: {session.practice_date}",
            "=" * 60,
            "",
        ]
        per_line = 5
        for row_start in range(0, len(session.exercises), per_line):
            chunk = session.exercises[row_start : row_start + per_line]
            parts = []
            for ex in chunk:
                if with_answers:
                    parts.append(f"{ex.expression}={ex.correct_answer}")
                else:
                    parts.append(f"{ex.expression}=")
            lines.append("    ".join(f"{p:<14}" for p in parts))
            lines.append("")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
