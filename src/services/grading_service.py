"""判题服务（重构后）。"""

from __future__ import annotations

from pathlib import Path

from src.contracts import ensure, require
from src.exceptions import ValidationError
from src.models import GradeDetail, GradeResult, PracticeSession, StudentAnswer
from src.parsers import parse_answer_line, parse_expression
from src.repositories.csv_practice_repository import CsvPracticeRepository


class GradingService:
    def __init__(self, repository: CsvPracticeRepository) -> None:
        self._repository = repository

    def grade_session(self, session_id: str) -> GradeResult:
        practice = self._repository.load_practice(session_id)
        answers = self._repository.load_answers(session_id)
        return self.grade(practice, answers, persist=True)

    def grade(
        self,
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
            self._repository.save_grade_result(result)
        return result

    def parse_answers_from_file(
        self,
        path: Path,
        practice: PracticeSession,
    ) -> list[StudentAnswer]:
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

    def import_and_grade(self, session_id: str, answer_file: Path) -> GradeResult:
        practice = self._repository.load_practice(session_id)
        answers = self.parse_answers_from_file(answer_file, practice)
        self._repository.save_answers(session_id, answers)
        return self.grade(practice, answers, persist=True)
