"""交互式口算练习：小明在电脑上逐题作答并即时批改。"""

from __future__ import annotations

from src.exceptions import NotFoundError, ValidationError
from src.generator import (
    display_type_name,
    generate_practice,
    practice_type_from_menu_choice,
)
from src.grader import grade
from src.io.console import TextIO
from src.models import StudentAnswer
from src.repository import list_session_ids, load_practice, save_answers, save_practice


def _read_int_answer(io: TextIO, prompt: str) -> int:
    """防御性读取整数答案，处理输入格式错误。"""
    while True:
        raw = io.prompt(prompt)
        try:
            return int(raw.strip())
        except ValueError:
            io.println("  请输入整数，请重试。")


def collect_answers(practice, io: TextIO) -> list[StudentAnswer]:
    """逐题收集学生答案。"""
    answers: list[StudentAnswer] = []
    total = practice.total
    io.println(f"\n开始练习，共 {total} 题。输入数字答案，回车确认。")
    io.println("提示: 输入 q 可放弃本次练习。\n")
    for ex in practice.exercises:
        while True:
            raw = io.prompt(f"第 {ex.seq:>2}/{total} 题   {ex.expression}=")
            if raw.strip().lower() == "q":
                raise ValidationError("已取消本次练习。")
            try:
                value = int(raw.strip())
                break
            except ValueError:
                io.println("  请输入整数答案。")
        answers.append(
            StudentAnswer(seq=ex.seq, expression=ex.expression, student_answer=value)
        )
    return answers


def run_interactive_practice(io: TextIO) -> None:
    """
    交互练习主流程：
    1. 选择新题或已有练习卷
    2. 逐题输入答案
    3. 自动判题、保存 CSV
    """
    io.println("\n--- 交互式口算练习 (小明) ---")
    io.println("  1. 开始新练习 (即时出题)")
    io.println("  2. 使用已有练习卷")
    mode = io.prompt("请选择", "1")

    if mode == "2":
        ids = list_session_ids()
        if not ids:
            raise NotFoundError("尚无练习卷，请华经理先生成或选择「开始新练习」。")
        io.println("可选练习卷：")
        for i, sid in enumerate(ids[:10], start=1):
            io.println(f"  {i}. {sid}")
        choice = io.prompt("输入 session_id 或序号", ids[0])
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ids):
                session_id = ids[idx]
            else:
                session_id = choice
        else:
            session_id = choice
        practice = load_practice(session_id)
    else:
        io.println("练习类型: 1=加法  2=减法  3=加减混合")
        ptype = practice_type_from_menu_choice(io.prompt("请选择", "3"))
        count_raw = io.prompt("题量 (默认50，可填10便于试做)", "50")
        try:
            count = int(count_raw)
        except ValueError:
            raise ValidationError("题量必须是整数")
        practice = generate_practice(ptype, count=count)
        save_practice(practice)
        io.println(f"已生成练习卷: {practice.session_id}")

    answers = collect_answers(practice, io)
    save_answers(practice.session_id, answers)
    result = grade(practice, answers, persist=True)

    io.println("\n" + "=" * 40)
    io.println(f"  练习完成！得分: {result.score}  ({result.correct}/{result.total})")
    io.println("=" * 40)
    if result.wrong_expressions:
        io.println("\n错题回顾：")
        wrong_set = set(result.wrong_expressions)
        for d in result.details:
            if not d.is_correct:
                io.println(
                    f"  {d.expression} = {d.student_answer}  "
                    f"(正确答案 {d.correct_answer})"
                )
    else:
        io.println("\n全部正确，太棒了！")
    io.println(f"\n成绩已保存，类型: {display_type_name(practice.practice_type)}")
