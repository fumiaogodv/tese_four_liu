#!/usr/bin/env python3
"""
口算练习系统 — 唯一启动入口 main()

整合故事1~6：出题、导出、批改、统计、交互练习。
"""


def main() -> None:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from src.app import run

    run()


if __name__ == "__main__":
    main()
