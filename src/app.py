"""命令行交互：华经理使用流程的主入口。"""

from __future__ import annotations

from pathlib import Path

from src.analyzer import analyze, format_results_table
from src.constants import menu_actions
from src.exceptions import NotFoundError, OralCalcError, ValidationError
from src.export import export_practice_text
from src.generator import (
    display_type_name,
    generate_practice,
    practice_type_from_menu_choice,
)
from src.grader import grade_session, import_answers_and_grade
from src.repository import DATA_DIR, list_session_ids, load_all_results, load_practice, save_practice


def _prompt(msg: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{msg}{suffix}: ").strip()
    return value or default


def _choose_session_id() -> str:
    ids = list_session_ids()
    if not ids:
        raise NotFoundError("尚无练习卷，请先生成练习。")
    print("可选练习卷：")
    for i, sid in enumerate(ids[:10], start=1):
        print(f"  {i}. {sid}")
    choice = _prompt("输入 session_id 或序号", ids[0])
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(ids):
            return ids[idx]
    return choice


def cmd_create_practice() -> None:
    print("练习类型: 1=加法  2=减法  3=加减混合")
    ptype = practice_type_from_menu_choice(_prompt("请选择", "1"))
    session = generate_practice(ptype)
    save_practice(session)
    out = DATA_DIR / "export" / f"{session.session_id}_练习.txt"
    export_practice_text(session, out, with_answers=False)
    ans = DATA_DIR / "export" / f"{session.session_id}_答案.txt"
    export_practice_text(session, ans, with_answers=True)
    print(f"\n已生成: {display_type_name(ptype)}")
    print(f"  session_id: {session.session_id}")
    print(f"  题目数: {session.total}")
    print(f"  CSV: data/practices.csv")
    print(f"  打印文件: {out}")
    print(f"  标准答案: {ans}")


def cmd_export_practice_text() -> None:
    session_id = _choose_session_id()
    session = load_practice(session_id)
    out = Path(_prompt("导出路径", str(DATA_DIR / "export" / f"{session_id}_练习.txt")))
    export_practice_text(session, out, with_answers=False)
    print(f"已导出到: {out}")


def cmd_import_and_grade() -> None:
    session_id = _choose_session_id()
    default = str(DATA_DIR / "samples" / f"{session_id}_学生答案.txt")
    path = Path(_prompt("答案文件路径", default))
    result = import_answers_and_grade(session_id, path)
    print(f"\n判题完成: {result.correct}/{result.total} 正确, 得分 {result.score}")
    if result.wrong_expressions:
        print("错题:", ", ".join(result.wrong_expressions[:10]))
        if len(result.wrong_expressions) > 10:
            print(f"  ... 共 {len(result.wrong_expressions)} 道")
    print("成绩已写入 data/results.csv")


def cmd_list_results() -> None:
    results = load_all_results()
    print(format_results_table(results))


def cmd_analyze_wrong() -> None:
    print(analyze())


def cmd_show_session_detail() -> None:
    session_id = _choose_session_id()
    session = load_practice(session_id)
    try:
        result = grade_session(session_id)
        graded = True
    except NotFoundError:
        graded = False
        result = None

    print(f"\n练习卷 {session_id}")
    print(f"  日期: {session.practice_date}  类型: {display_type_name(session.practice_type)}")
    print(f"  题量: {session.total}")
    if graded and result:
        print(f"  成绩: {result.score} ({result.correct}/{result.total})")
        if result.wrong_expressions:
            print("  错题:", ", ".join(result.wrong_expressions))
    else:
        print("  （尚未导入答案判题）")
    show = _prompt("显示全部题目? y/N", "n").lower() == "y"
    if show:
        for ex in session.exercises:
            print(f"  {ex.seq:2d}. {ex.expression} = {ex.correct_answer}")


_HANDLERS = {
    "create_practice": cmd_create_practice,
    "export_practice_text": cmd_export_practice_text,
    "import_and_grade": cmd_import_and_grade,
    "list_results": cmd_list_results,
    "analyze_wrong": cmd_analyze_wrong,
    "show_session_detail": cmd_show_session_detail,
}


def run() -> None:
    print("=" * 50)
    print("  口算练习 · 数据处理（华经理端）")
    print("=" * 50)
    while True:
        print()
        for action in menu_actions():
            print(f"  [{action.key}] {action.title}")
        choice = _prompt("\n请选择功能", "0")
        if choice == "0":
            print("再见。")
            break
        action = next((a for a in menu_actions() if a.key == choice), None)
        if not action:
            print("无效选项，请重新输入。")
            continue
        if action.handler_name == "exit":
            break
        handler = _HANDLERS.get(action.handler_name)
        if not handler:
            print("功能未实现。")
            continue
        try:
            handler()
        except OralCalcError as e:
            print(f"\n错误: {e}")
        except KeyboardInterrupt:
            print("\n已取消。")
