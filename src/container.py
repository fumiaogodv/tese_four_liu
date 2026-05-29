"""依赖注入容器：组装仓储与各业务服务。"""

from __future__ import annotations

from pathlib import Path

from src.paths import get_data_dir
from src.repositories.csv_practice_repository import CsvPracticeRepository
from src.services.analysis_service import AnalysisService
from src.services.export_service import ExportService
from src.services.grading_service import GradingService
from src.services.interactive_service import InteractivePracticeService
from src.services.practice_generator import PracticeGeneratorService


class ServiceContainer:
    """应用服务容器（重构后统一装配点）。"""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or get_data_dir()
        self.repository = CsvPracticeRepository(self.data_dir)
        self.generator = PracticeGeneratorService(self.repository)
        self.grader = GradingService(self.repository)
        self.analyzer = AnalysisService(self.repository)
        self.export = ExportService()
        self.interactive = InteractivePracticeService(
            self.generator, self.grader, self.repository
        )


_default_container: ServiceContainer | None = None


def get_container(data_dir: Path | None = None) -> ServiceContainer:
    global _default_container
    if data_dir is not None:
        return ServiceContainer(data_dir)
    if _default_container is None:
        _default_container = ServiceContainer()
    return _default_container


def reset_container() -> None:
    global _default_container
    _default_container = None
