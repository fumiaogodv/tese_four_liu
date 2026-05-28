#!/usr/bin/env python3
"""口算练习数据处理系统 — 启动入口。"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app import run  # noqa: E402


if __name__ == "__main__":
    run()
