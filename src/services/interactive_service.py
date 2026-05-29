"""交互式口算练习服务（重构后）。"""

from __future__ import annotations

from src.exceptions import NotFoundError, ValidationError
from src.io.console import TextIO
from src.models import PracticeSession, StudentAnswer
from src.repositories.csv_practice_repository import CsvPracticeRepository
from src.services.grading_service import GradingService
from src.services.practice_generator import PracticeGeneratorService


class InteractivePracticeService:
    def __init__(
        self,
        generator: PracticeGeneratorService,
        grader: GradingService,
        repository: CsvPracticeRepository,
    ) -> None:
        self._generator = generator
        self._grader = grader
        self._repository = repository

    def collect_answers(self, practice: PracticeSession, io: TextIO) -> list[StudentAnswer]:
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

    def run(self, io: TextIO) -> None:
        io.println("\n--- 交互式口算练习 (小明) ---")
        io.println("  1. 开始新练习 (即时出题)")
        io.println("  2. 使用已有练习卷")
        mode = io.prompt("请选择", "1")

        if mode == "2":
            ids = self._repository.list_session_ids()
            if not ids:
                raise NotFoundError("尚无练习卷，请华经理先生成或选择「开始新练习」。")
            io.println("可选练习卷：")
            for i, sid in enumerate(ids[:10], start=1):
                io.println(f"  {i}. {sid}")
            choice = io.prompt("输入 session_id 或序号", ids[0])
            if choice.isdigit():
                idx = int(choice) - 1
                session_id = ids[idx] if 0 <= idx < len(ids) else choice
            else:
                session_id = choice
            practice = self._repository.load_practice(session_id)
        else:
            io.println("练习类型: 1=加法  2=减法  3=加减混合")
            ptype = PracticeGeneratorService.practice_type_from_choice(io.prompt("请选择", "3"))
            count_raw = io.prompt("题量 (默认50，可填10便于试做)", "50")
            try:
                count = int(count_raw)
            except ValueError:
                raise ValidationError("题量必须是整数")
            practice = self._generator.generate(ptype, count=count)
            self._repository.save_practice(practice)
            io.println(f"已生成练习卷: {practice.session_id}")

        answers = self.collect_answers(practice, io)
        self._repository.save_answers(practice.session_id, answers)
        result = self._grader.grade(practice, answers, persist=True)

        io.println("\n" + "=" * 40)
        io.println(f"  练习完成！得分: {result.score}  ({result.correct}/{result.total})")
        io.println("=" * 40)
        if result.wrong_expressions:
            io.println("\n错题回顾：")
            for d in result.details:
                if not d.is_correct:
                    io.println(
                        f"  {d.expression} = {d.student_answer}  "
                        f"(正确答案 {d.correct_answer})"
                    )
        else:
            io.println("\n全部正确，太棒了！")
        io.println(
            f"\n成绩已保存，类型: "
            f"{PracticeGeneratorService.display_type_name(practice.practice_type)}"
        )
