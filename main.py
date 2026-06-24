#!/usr/bin/env python3
"""
口算练习系统 — 唯一启动入口 main()

默认启动 GUI；使用 --cli 进入命令行界面。
"""


def main() -> None:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    if "--cli" in sys.argv:
        from src.app import run

        run()
    else:
        from src.gui.main_window import run_gui

        run_gui()


if __name__ == "__main__":
    main()
