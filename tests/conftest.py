"""pytest 全局配置：每个测试使用独立数据目录与服务容器。"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    from src.container import get_container, reset_container

    reset_container()
    monkeypatch.setattr("src.paths.get_data_dir", lambda: tmp_path)
    monkeypatch.setattr("src.repository.DATA_DIR", tmp_path)
    get_container(tmp_path)
    yield
    reset_container()
