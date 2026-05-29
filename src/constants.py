"""表驱动配置：菜单、练习类型、约束、CSV 列名等集中定义。"""

from __future__ import annotations

from dataclasses import dataclass

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

# 统一主菜单（故事6 / 图5.1）：前5项华经理，第6项小明
MAIN_MENU_ITEMS: list[tuple[str, str, str, str]] = [
    ("1", "批量生成练习题", "create_practice", "manager"),
    ("2", "挑选并导出练习卷", "export_practice", "manager"),
    ("3", "导入答案并批改", "import_and_grade", "manager"),
    ("4", "查看练习成绩统计", "list_results", "manager"),
    ("5", "错题与薄弱题目分析", "analyze_wrong", "manager"),
    ("6", "交互式口算练习", "interactive_practice", "student"),
    ("0", "退出", "exit", "all"),
]

# 兼容第4部分旧引用
MENU_ITEMS: list[tuple[str, str, str]] = [
    (k, t, h) for k, t, h, _ in MAIN_MENU_ITEMS if h != "interactive_practice"
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
class MainMenuAction:
    key: str
    title: str
    handler_name: str
    role: str  # manager | student | all


@dataclass(frozen=True)
class MenuAction:
    key: str
    title: str
    handler_name: str


def main_menu_actions() -> list[MainMenuAction]:
    return [MainMenuAction(k, t, h, r) for k, t, h, r in MAIN_MENU_ITEMS]


def menu_actions() -> list[MenuAction]:
    return [MenuAction(k, t, h) for k, t, h in MAIN_MENU_ITEMS if h != "exit"]
