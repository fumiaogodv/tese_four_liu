"""华经理端功能处理：整合故事1~4 与数据处理模块。"""

from __future__ import annotations

from pathlib import Path

from src.analyzer import analyze, format_results_table
from src.exceptions import NotFoundError
from src.export import export_practice_text
from src.generator import (
    display_type_name,
    generate_practice,
    practice_type_from_menu_choice,
)
from src.grader import grade_session, import_answers_and_grade
from src.io.console import TextIO
from src.repository import DATA_DIR, list_session_ids, load_all_results, load_practice, save_practice


def _choose_session_id(io: TextIO) -> str:
    ids = list_session_ids()
    if not ids:
        raise NotFoundError("尚无练习卷，请先使用功能1生成练习。")
    io.println("可选练习卷：")
    for i, sid in enumerate(ids[:10], start=1):
        io.println(f"  {i}. {sid}")
    choice = io.prompt("输入 session_id 或序号", ids[0])
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(ids):
            return ids[idx]
    return choice


def cmd_create_practice(io: TextIO) -> None:
    io.println("\n--- 批量生成练习题 ---")
    io.println("练习类型: 1=加法  2=减法  3=加减混合")
    ptype = practice_type_from_menu_choice(io.prompt("请选择", "1"))
    session = generate_practice(ptype)
    save_practice(session)
    out = DATA_DIR / "export" / f"{session.session_id}_练习.txt"
    export_practice_text(session, out, with_answers=False)
    ans = DATA_DIR / "export" / f"{session.session_id}_答案.txt"
    export_practice_text(session, ans, with_answers=True)
    io.println(f"\n已生成: {display_type_name(ptype)}")
    io.println(f"  session_id: {session.session_id}")
    io.println(f"  题目数: {session.total} (每行5题, 共{session.total // 5}行)")
    io.println(f"  CSV: data/practices.csv")
    io.println(f"  打印文件: {out}")
    io.println(f"  标准答案: {ans}")


def cmd_export_practice(io: TextIO) -> None:
    io.println("\n--- 挑选并导出练习卷 ---")
    session_id = _choose_session_id(io)
    session = load_practice(session_id)
    default = str(DATA_DIR / "export" / f"{session_id}_练习.txt")
    out = Path(io.prompt("导出路径", default))
    export_practice_text(session, out, with_answers=False)
    io.println(f"已导出到: {out}")


def cmd_import_and_grade(io: TextIO) -> None:
    io.println("\n--- 导入答案并批改 ---")
    session_id = _choose_session_id(io)
    default = str(DATA_DIR / "samples" / f"{session_id}_学生答案.txt")
    path = Path(io.prompt("答案文件路径", default))
    result = import_answers_and_grade(session_id, path)
    io.println(f"\n判题完成: {result.correct}/{result.total} 正确, 得分 {result.score}")
    if result.wrong_expressions:
        io.println("错题:", ", ".join(result.wrong_expressions[:10]))
        if len(result.wrong_expressions) > 10:
            io.println(f"  ... 共 {len(result.wrong_expressions)} 道")
    io.println("成绩已写入 data/results.csv")


def cmd_list_results(io: TextIO) -> None:
    io.println("\n--- 练习成绩统计 ---")
    results = load_all_results()
    io.println(format_results_table(results))


def cmd_analyze_wrong(io: TextIO) -> None:
    io.println("\n--- 错题与薄弱题目分析 ---")
    io.println(analyze())


def cmd_show_session_detail(io: TextIO) -> None:
    io.println("\n--- 单次练习详情 ---")
    session_id = _choose_session_id(io)
    session = load_practice(session_id)
    try:
        result = grade_session(session_id)
        graded = True
    except NotFoundError:
        graded = False
        result = None

    io.println(f"\n练习卷 {session_id}")
    io.println(f"  日期: {session.practice_date}  类型: {display_type_name(session.practice_type)}")
    io.println(f"  题量: {session.total}")
    if graded and result:
        io.println(f"  成绩: {result.score} ({result.correct}/{result.total})")
        if result.wrong_expressions:
            io.println("  错题:", ", ".join(result.wrong_expressions))
    else:
        io.println("  （尚未导入答案或完成交互练习）")
    show = io.prompt("显示全部题目? y/N", "n").lower() == "y"
    if show:
        for ex in session.exercises:
            io.println(f"  {ex.seq:2d}. {ex.expression} = {ex.correct_answer}")


HANDLERS = {
    "create_practice": cmd_create_practice,
    "export_practice": cmd_export_practice,
    "import_and_grade": cmd_import_and_grade,
    "list_results": cmd_list_results,
    "analyze_wrong": cmd_analyze_wrong,
    "show_session_detail": cmd_show_session_detail,
}
