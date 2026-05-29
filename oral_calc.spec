# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置：生成单文件可执行程序。"""

import sys
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)

a = Analysis(
    [str(root / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "data" / "samples"), "data/samples"),
    ],
    hiddenimports=[
        "src",
        "src.app",
        "src.container",
        "src.commands.manager_commands",
        "src.repositories.csv_practice_repository",
        "src.services.practice_generator",
        "src.services.grading_service",
        "src.services.analysis_service",
        "src.services.export_service",
        "src.services.interactive_service",
        "src.services.session_id",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="口算练习系统",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
