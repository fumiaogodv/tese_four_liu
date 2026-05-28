"""表驱动配置：菜单、练习类型、约束、CSV 列名等集中定义。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

# 练习类型 -> 生成策略键
PRACTICE_TYPE_LABELS: dict[str, str] = {
    "1": "addition",
    "2": "subtraction",
    "3": "mixed",
}

PRACTICE_TYPE_NAMES: dict[str, str] = {
    "addition": "加法练习",
    "subtraction": "减法练习",
    "mixed": "加减混合练习",
}

# 生成约束（表驱动，避免散落魔法数）
GENERATION_RULES: dict[str, dict[str, int]] = {
    "addition": {"max_sum": 100, "count": 50},
    "subtraction": {"min_diff": 0, "count": 50},
    "mixed": {"max_sum": 100, "min_diff": 0, "count": 50},
}

# 主菜单：编号 -> (标题, 处理函数名)
MENU_ITEMS: list[tuple[str, str, str]] = [
    ("1", "生成练习卷并保存(CSV)", "create_practice"),
    ("2", "导出练习卷到文本(便于打印)", "export_practice_text"),
    ("3", "导入学生答案并自动判题", "import_and_grade"),
    ("4", "查看练习成绩列表", "list_results"),
    ("5", "分析错题与薄弱题目", "analyze_wrong"),
    ("6", "按日期查看单次练习详情", "show_session_detail"),
    ("0", "退出", "exit"),
]

# CSV 表头（契约：列名固定）
CSV_PRACTICE_HEADERS = [
    "session_id",
    "date",
    "practice_type",
    "seq",
    "expression",
    "correct_answer",
]

CSV_ANSWER_HEADERS = [
    "session_id",
    "seq",
    "expression",
    "student_answer",
]

CSV_RESULT_HEADERS = [
    "session_id",
    "date",
    "practice_type",
    "total",
    "correct",
    "score",
    "wrong_expressions",
]

CSV_WRONG_STAT_HEADERS = [
    "expression",
    "wrong_count",
    "last_session_id",
]


@dataclass(frozen=True)
class MenuAction:
    key: str
    title: str
    handler_name: str


def menu_actions() -> list[MenuAction]:
    return [MenuAction(k, t, h) for k, t, h in MENU_ITEMS]
