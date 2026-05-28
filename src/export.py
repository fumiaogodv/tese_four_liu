"""导出练习卷/答案卷文本：每行5题，共10行（50题）。"""

from __future__ import annotations

from pathlib import Path

from src.generator import display_type_name
from src.models import PracticeSession


def export_practice_text(session: PracticeSession, path: Path, *, with_answers: bool = False) -> None:
    """生成可打印文本：题目卷或答案卷。"""
    title = (
        f"【答案卷】{display_type_name(session.practice_type)}"
        if with_answers
        else f"【练习卷】{display_type_name(session.practice_type)}"
    )
    lines = [
        title,
        f"编号: {session.session_id}  日期: {session.practice_date}",
        "=" * 60,
        "",
    ]
    per_line = 5
    items = session.exercises
    for row_start in range(0, len(items), per_line):
        chunk = items[row_start : row_start + per_line]
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
