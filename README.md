# 口算练习系统（软件构造案例 第4~8部分）

整合故事1~8：CLI + **GUI 图形界面**、数据处理、交互练习、重构交付、可执行打包。

## 快速开始

### GUI 模式（默认，故事8）

```powershell
cd C:\Users\godv\Desktop\vibe_coding\test_four_liu
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### CLI 命令行模式

```powershell
python main.py --cli
```

### 打包为 exe

```powershell
.\scripts\build.ps1
# 输出: dist\口算练习系统.exe（GUI 无黑窗口）
```

## GUI 功能（第7部分）

左侧导航：生成 / 导出 / 导入批改 / 成绩 / 错题分析 / 小明口算练习。鼠标完成主要操作。

## 测试

```powershell
pytest tests/ -v
```

GUI 通过 `GuiController` 单元测试，无需启动窗口。

## 文档索引

| 部分 | 文档 |
|------|------|
| 第7部分 GUI | [GUI_DESIGN.md](docs/GUI_DESIGN.md), [GUI_CLASS_DIAGRAM.md](docs/GUI_CLASS_DIAGRAM.md) |
| 第5部分 用户交互 | [UI_PROTOTYPE.md](docs/UI_PROTOTYPE.md) |
| 第7部分 重构交付 | [REFACTORING.md](docs/REFACTORING.md), [BUILD.md](docs/BUILD.md) |
| 第4部分 数据处理 | [DESIGN.md](docs/DESIGN.md) |

## 目录结构

```
main.py                 # 默认 GUI，--cli 为命令行
src/gui/                # 图形界面（观察者 + MVC）
src/services/           # 业务服务
src/repositories/       # CSV 仓储
tests/                  # 含 test_gui_controller.py
```
