"""应用路径：开发模式与 PyInstaller 打包后均可正确定位 data 目录。"""

from __future__ import annotations

import sys
from pathlib import Path


def get_app_root() -> Path:
    """可执行文件或项目根目录。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    """数据目录（CSV、导出文件）；不存在则创建。"""
    data = get_app_root() / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "export").mkdir(exist_ok=True)
    (data / "samples").mkdir(exist_ok=True)
    return data
