"""判题服务：比对标准答案与学生答案。"""

from __future__ import annotations

from pathlib import Path

from src.contracts import ensure, require
from src.exceptions import ValidationError
from src.models import GradeDetail, GradeResult, PracticeSession, StudentAnswer
from src.parsers import parse_answer_line, parse_expression
from src.repository import load_answers, load_practice, save_answers, save_grade_result


def grade_session(session_id: str) -> GradeResult:
    """根据已保存的答案判题并写入 results.csv。"""
    practice = load_practice(session_id)
    answers = load_answers(session_id)
    return grade(practice, answers, persist=True)


def grade(
    practice: PracticeSession,
    answers: list[StudentAnswer],
    *,
    persist: bool = False,
) -> GradeResult:
    require(len(answers) == practice.total, "答案数量须与题目一致")

    answer_map = {a.expression: a for a in answers}
    details: list[GradeDetail] = []
    correct_count = 0

    for ex in practice.exercises:
        if ex.expression not in answer_map:
            raise ValidationError(f"缺少题目答案: {ex.expression}")
        sa = answer_map[ex.expression]
        require(sa.seq == ex.seq, f"题号与算式不匹配: seq={sa.seq} {ex.expression}")
        ok = sa.student_answer == ex.correct_answer
        if ok:
            correct_count += 1
        details.append(
            GradeDetail(
                seq=ex.seq,
                expression=ex.expression,
                correct_answer=ex.correct_answer,
                student_answer=sa.student_answer,
                is_correct=ok,
            )
        )

    result = GradeResult(
        session_id=practice.session_id,
        practice_date=practice.practice_date,
        practice_type=practice.practice_type,
        total=practice.total,
        correct=correct_count,
        details=details,
    )
    ensure(result.correct + len(result.wrong_expressions) == result.total, "统计一致")
    if persist:
        save_grade_result(result)
    return result


def parse_answers_from_file(
    path: Path,
    practice: PracticeSession,
) -> list[StudentAnswer]:
    """从文本文件解析答案行，并与练习卷对齐。"""
    require(path.exists(), f"文件不存在: {path}")
    expr_to_seq = {ex.expression: ex for ex in practice.exercises}
    answers: list[StudentAnswer] = []
    errors: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ValidationError(f"无法读取文件: {e}") from e

    for i, line in enumerate(text.splitlines(), start=1):
        try:
            expr, student_ans = parse_answer_line(line)
        except ValidationError:
            continue
        if expr not in expr_to_seq:
            errors.append(f"第{i}行: 算式不在本卷中 {expr}")
            continue
        ex = expr_to_seq[expr]
        # 校验算式合法（契约与生成规则一致）
        _, _, _, expected = parse_expression(expr)
        if expected != ex.correct_answer:
            errors.append(f"第{i}行: 算式与题库不一致 {expr}")
            continue
        answers.append(
            StudentAnswer(seq=ex.seq, expression=expr, student_answer=student_ans)
        )

    if errors:
        raise ValidationError("\n".join(errors[:10]))
    require(len(answers) == practice.total, f"有效答案 {len(answers)} 道，需要 {practice.total} 道")
    return answers


def import_answers_and_grade(session_id: str, answer_file: Path) -> GradeResult:
    practice = load_practice(session_id)
    answers = parse_answers_from_file(answer_file, practice)
    save_answers(session_id, answers)
    return grade(practice, answers, persist=True)
