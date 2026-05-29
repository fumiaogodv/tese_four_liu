# 口算练习系统（软件构造案例 第4~7部分）

整合故事1~7：统一 CLI、数据处理、交互练习、**面向对象重构**、**可执行程序打包**。

## 快速开始

### 开发模式

```powershell
cd c:\Users\godv\Desktop\vibe_coding\test_four_liu
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### 打包为 exe（故事7）

```powershell
.\scripts\build.ps1
# 输出: dist\口算练习系统.exe
```

复制 exe 到任意 Windows 机器即可运行，无需安装 Python。详见 [docs/BUILD.md](docs/BUILD.md)。

## 主菜单

| 编号 | 角色 | 功能 |
|------|------|------|
| 1~5 | 华经理 | 生成 / 导出 / 批改 / 统计 / 错题分析 |
| 6 | 小明 | 交互式口算练习 |
| 0 | — | 退出 |

## 测试（TDD / 回归）

```powershell
pytest tests/ -v
```

## 文档索引

| 部分 | 文档 |
|------|------|
| 第4部分 数据处理 | [DESIGN.md](docs/DESIGN.md), [FLOW.md](docs/FLOW.md) |
| 第5部分 用户交互 | [UI_PROTOTYPE.md](docs/UI_PROTOTYPE.md), [CLASS_DIAGRAM.md](docs/CLASS_DIAGRAM.md) |
| 第7部分 重构与交付 | [REFACTORING.md](docs/REFACTORING.md), [TDD.md](docs/TDD.md), [BUILD.md](docs/BUILD.md) |

## 重构后目录结构

```
main.py                     # 唯一入口
src/
  container.py              # 依赖注入容器
  paths.py                  # 开发/打包双模式路径
  repositories/             # 仓储层
  services/                 # 业务服务层
  commands/                 # 命令模式（菜单功能）
  app.py                    # Application 主循环
oral_calc.spec              # PyInstaller 配置
scripts/build.ps1           # 一键打包
tests/                      # 单元测试 + TDD 示例
```

## 编程规范

- 提交信息：`feat:` / `fix:` / `refactor:` / `docs:` + 简述
- 新功能先写测试（TDD）再实现
- 不提交 `venv/`、`dist/`、`build/`
