"""华经理端与小明端命令实现。"""

from __future__ import annotations

from pathlib import Path

from src.commands.base import Command
from src.container import ServiceContainer
from src.exceptions import NotFoundError
from src.io.console import TextIO
from src.services.practice_generator import PracticeGeneratorService


def _choose_session_id(io: TextIO, services: ServiceContainer) -> str:
    ids = services.repository.list_session_ids()
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


class CreatePracticeCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        io.println("\n--- 批量生成练习题 ---")
        io.println("练习类型: 1=加法  2=减法  3=加减混合")
        ptype = PracticeGeneratorService.practice_type_from_choice(io.prompt("请选择", "1"))
        session = services.generator.generate(ptype)
        services.repository.save_practice(session)
        export_dir = services.repository.data_dir / "export"
        out = export_dir / f"{session.session_id}_练习.txt"
        ans = export_dir / f"{session.session_id}_答案.txt"
        services.export.export_practice_text(session, out, with_answers=False)
        services.export.export_practice_text(session, ans, with_answers=True)
        io.println(f"\n已生成: {PracticeGeneratorService.display_type_name(ptype)}")
        io.println(f"  session_id: {session.session_id}")
        io.println(f"  题目数: {session.total} (每行5题, 共{session.total // 5}行)")
        io.println("  CSV: data/practices.csv")
        io.println(f"  打印文件: {out}")
        io.println(f"  标准答案: {ans}")


class ExportPracticeCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        io.println("\n--- 挑选并导出练习卷 ---")
        session_id = _choose_session_id(io, services)
        session = services.repository.load_practice(session_id)
        default = str(services.repository.data_dir / "export" / f"{session_id}_练习.txt")
        out = Path(io.prompt("导出路径", default))
        services.export.export_practice_text(session, out, with_answers=False)
        io.println(f"已导出到: {out}")


class ImportAndGradeCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        io.println("\n--- 导入答案并批改 ---")
        session_id = _choose_session_id(io, services)
        default = str(services.repository.data_dir / "samples" / f"{session_id}_学生答案.txt")
        path = Path(io.prompt("答案文件路径", default))
        result = services.grader.import_and_grade(session_id, path)
        io.println(f"\n判题完成: {result.correct}/{result.total} 正确, 得分 {result.score}")
        if result.wrong_expressions:
            io.println("错题:", ", ".join(result.wrong_expressions[:10]))
            if len(result.wrong_expressions) > 10:
                io.println(f"  ... 共 {len(result.wrong_expressions)} 道")
        io.println("成绩已写入 data/results.csv")


class ListResultsCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        io.println("\n--- 练习成绩统计 ---")
        results = services.repository.load_all_results()
        io.println(services.analyzer.format_results_table(results))


class AnalyzeWrongCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        io.println("\n--- 错题与薄弱题目分析 ---")
        io.println(services.analyzer.analyze())


class InteractivePracticeCommand:
    def execute(self, io: TextIO, services: ServiceContainer) -> None:
        services.interactive.run(io)


class CommandRegistry:
    """表驱动命令注册表。"""

    def __init__(self, services: ServiceContainer) -> None:
        self._services = services
        self._commands: dict[str, Command] = {
            "create_practice": CreatePracticeCommand(),
            "export_practice": ExportPracticeCommand(),
            "import_and_grade": ImportAndGradeCommand(),
            "list_results": ListResultsCommand(),
            "analyze_wrong": AnalyzeWrongCommand(),
            "interactive_practice": InteractivePracticeCommand(),
        }

    def execute(self, handler_name: str, io: TextIO) -> None:
        command = self._commands.get(handler_name)
        if command is None:
            io.println("功能未实现。")
            return
        command.execute(io, self._services)
