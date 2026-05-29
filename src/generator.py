"""generator 兼容层。"""

from __future__ import annotations

from src.container import get_container
from src.models import PracticeSession
from src.services.practice_generator import PracticeGeneratorService


def generate_practice(
    practice_type: str,
    *,
    count: int | None = None,
    seed: int | None = None,
) -> PracticeSession:
    return get_container().generator.generate(practice_type, count=count, seed=seed)


def practice_type_from_menu_choice(choice: str) -> str:
    return PracticeGeneratorService.practice_type_from_choice(choice)


def display_type_name(practice_type: str) -> str:
    return PracticeGeneratorService.display_type_name(practice_type)
