"""控制台输入输出：隔离交互层，降低 I/O 故障影响范围。"""

from __future__ import annotations

from typing import Protocol, TextIO as TypingTextIO


class TextIO(Protocol):
    def prompt(self, message: str, default: str = "") -> str: ...
    def println(self, message: str = "") -> None: ...


class ConsoleIO:
    """标准控制台实现。"""

    def __init__(self, input_stream: TypingTextIO | None = None, output_stream: TypingTextIO | None = None) -> None:
        import sys

        self._input = input_stream or sys.stdin
        self._output = output_stream or sys.stdout

    def prompt(self, message: str, default: str = "") -> str:
        suffix = f" [{default}]" if default else ""
        self._output.write(f"{message}{suffix}: ")
        self._output.flush()
        try:
            value = self._input.readline()
        except (EOFError, OSError):
            return default
        if value is None:
            return default
        text = value.strip()
        return text or default

    def println(self, message: str = "") -> None:
        self._output.write(message + "\n")
        self._output.flush()
