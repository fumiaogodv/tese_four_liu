"""handlers 兼容层（已由 Command 模式替代，保留导出供参考）。"""

from src.commands.manager_commands import CommandRegistry

HANDLERS = {}  # 已废弃，请使用 CommandRegistry

__all__ = ["HANDLERS", "CommandRegistry"]
