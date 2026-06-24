"""GUI 控制器：封装业务逻辑，不依赖 tkinter，便于单元测试。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.container import ServiceContainer
from src.exceptions import NotFoundError, ValidationError
from src.gui.events import AppEvent, AppEventType, AppEventBus
from src.models import ExerciseItem, GradeResult, PracticeSession, StudentAnswer
from src.services.practice_generator import PracticeGeneratorService


@dataclass
class InteractiveSubmitResult:
    """交互练习单题提交结果。"""

    accepted: bool
    message: str
    is_complete: bool
    progress: tuple[int, int]  # current answered, total
    grade_result: GradeResult | None = None


@dataclass
class _InteractiveState:
    practice: PracticeSession
    index: int
    answers: list[StudentAnswer]


class GuiController:
    """GUI 与业务服务之间的控制器（MVC 中的 Controller）。"""

    def __init__(
        self,
        services: ServiceContainer,
        event_bus: AppEventBus | None = None,
    ) -> None:
        self._services = services
        self._bus = event_bus or AppEventBus()
        self._interactive: _InteractiveState | None = None

    @property
    def event_bus(self) -> AppEventBus:
        return self._bus

    @property
    def data_dir(self) -> Path:
        return self._services.data_dir

    def _status(self, message: str, event_type: AppEventType = AppEventType.STATUS) -> None:
        self._bus.notify(AppEvent(event_type, message))

    def list_sessions(self) -> list[str]:
        return self._services.repository.list_session_ids()

    def practice_type_choices(self) -> list[tuple[str, str]]:
        return [
            ("addition", "加法练习"),
            ("subtraction", "减法练习"),
            ("mixed", "加减混合练习"),
        ]

    def create_practice(self, practice_type: str) -> PracticeSession:
        session = self._services.generator.generate(practice_type)
        self._services.repository.save_practice(session)
        export_dir = self._services.repository.data_dir / "export"
        out = export_dir / f"{session.session_id}_练习.txt"
        ans = export_dir / f"{session.session_id}_答案.txt"
        self._services.export.export_practice_text(session, out, with_answers=False)
        self._services.export.export_practice_text(session, ans, with_answers=True)
        self._status(
            f"已生成练习卷 {session.session_id}，共 {session.total} 题",
            AppEventType.PRACTICE_CREATED,
        )
        self._bus.notify(
            AppEvent(AppEventType.SESSION_LIST_CHANGED, session.session_id, session)
        )
        return session

    def export_practice(self, session_id: str, path: Path | None = None) -> Path:
        session = self._services.repository.load_practice(session_id)
        if path is None:
            path = self._services.repository.data_dir / "export" / f"{session_id}_练习.txt"
        self._services.export.export_practice_text(session, path, with_answers=False)
        self._status(f"已导出到 {path}")
        return path

    def import_and_grade(self, session_id: str, answer_file: Path) -> GradeResult:
        result = self._services.grader.import_and_grade(session_id, answer_file)
        self._status(
            f"判题完成：{result.correct}/{result.total}，得分 {result.score}",
            AppEventType.GRADE_COMPLETED,
        )
        self._bus.notify(AppEvent(AppEventType.GRADE_COMPLETED, "", result))
        return result

    def get_results_text(self) -> str:
        results = self._services.repository.load_all_results()
        return self._services.analyzer.format_results_table(results)

    def get_analyze_text(self) -> str:
        return self._services.analyzer.analyze()

    def display_type_name(self, practice_type: str) -> str:
        return PracticeGeneratorService.display_type_name(practice_type)

    # --- 交互练习（小明）---

    def interactive_start_new(self, practice_type: str, count: int) -> PracticeSession:
        if count < 1 or count > 200:
            raise ValidationError("题量应在 1~200 之间")
        practice = self._services.generator.generate(practice_type, count=count)
        self._services.repository.save_practice(practice)
        self._interactive = _InteractiveState(practice, 0, [])
        self._bus.notify(
            AppEvent(AppEventType.INTERACTIVE_STARTED, practice.session_id, practice)
        )
        self._status(f"开始新练习：{practice.session_id}，共 {practice.total} 题")
        return practice

    def interactive_load(self, session_id: str) -> PracticeSession:
        practice = self._services.repository.load_practice(session_id)
        self._interactive = _InteractiveState(practice, 0, [])
        self._bus.notify(
            AppEvent(AppEventType.INTERACTIVE_STARTED, session_id, practice)
        )
        self._status(f"加载练习卷：{session_id}，共 {practice.total} 题")
        return practice

    def interactive_current(self) -> ExerciseItem | None:
        if self._interactive is None:
            return None
        if self._interactive.index >= self._interactive.practice.total:
            return None
        return self._interactive.practice.exercises[self._interactive.index]

    def interactive_progress(self) -> tuple[int, int]:
        if self._interactive is None:
            return 0, 0
        return self._interactive.index, self._interactive.practice.total

    def interactive_is_active(self) -> bool:
        return self._interactive is not None and self._interactive.index < (
            self._interactive.practice.total if self._interactive else 0
        )

    def interactive_submit_answer(self, raw: str) -> InteractiveSubmitResult:
        if self._interactive is None:
            raise ValidationError("请先开始或加载练习。")
        ex = self.interactive_current()
        if ex is None:
            raise ValidationError("练习已完成。")
        try:
            value = int(raw.strip())
        except ValueError:
            return InteractiveSubmitResult(
                accepted=False,
                message="请输入整数答案",
                is_complete=False,
                progress=self.interactive_progress(),
            )

        self._interactive.answers.append(
            StudentAnswer(seq=ex.seq, expression=ex.expression, student_answer=value)
        )
        self._interactive.index += 1
        total = self._interactive.practice.total
        answered = self._interactive.index
        self._bus.notify(
            AppEvent(
                AppEventType.INTERACTIVE_ANSWERED,
                f"第 {ex.seq} 题已提交",
                (answered, total),
            )
        )

        if answered >= total:
            practice = self._interactive.practice
            self._services.repository.save_answers(practice.session_id, self._interactive.answers)
            result = self._services.grader.grade(
                practice, self._interactive.answers, persist=True
            )
            self._interactive = None
            self._bus.notify(AppEvent(AppEventType.INTERACTIVE_FINISHED, "", result))
            self._bus.notify(AppEvent(AppEventType.GRADE_COMPLETED, "", result))
            self._status(f"练习完成！得分 {result.score}")
            return InteractiveSubmitResult(
                accepted=True,
                message="全部完成！",
                is_complete=True,
                progress=(total, total),
                grade_result=result,
            )

        return InteractiveSubmitResult(
            accepted=True,
            message=f"第 {ex.seq} 题已记录，请继续",
            is_complete=False,
            progress=(answered, total),
        )

    def interactive_cancel(self) -> None:
        self._interactive = None
        self._status("已取消当前练习")
