"""session_id 生成（TDD 提取的独立组件）。"""

from __future__ import annotations

from datetime import date


class SessionIdBuilder:
    """根据日期、练习类型与已有编号生成唯一 session_id。"""

    def build(
        self,
        practice_type: str,
        day: date | None = None,
        existing_ids: set[str] | None = None,
    ) -> str:
        d = day or date.today()
        base = f"{d.strftime('%Y%m%d')}_{practice_type[:3]}"
        taken = existing_ids or set()
        if base not in taken:
            return base
        n = 2
        while f"{base}_{n}" in taken:
            n += 1
        return f"{base}_{n}"
