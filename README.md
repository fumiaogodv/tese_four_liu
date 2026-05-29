# 口算练习系统（软件构造案例 第4~5部分）

整合故事1~6：**出题、导出、批改、统计、交互练习**，单一 `main()` 入口。

## 环境

```powershell
cd c:\Users\godv\Desktop\vibe_coding\test_four_liu
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 运行（唯一入口）

```powershell
python main.py
```

### 主菜单（图 5.1）

| 编号 | 角色 | 功能 |
|------|------|------|
| 1 | 华经理 | 批量生成练习题 |
| 2 | 华经理 | 挑选并导出练习卷 |
| 3 | 华经理 | 导入答案并批改 |
| 4 | 华经理 | 查看练习成绩统计 |
| 5 | 华经理 | 错题与薄弱题目分析 |
| 6 | 小明 | **交互式口算练习**（机上作答、即时批改） |
| 0 | — | 退出 |

## 测试

```powershell
pytest tests/ -v
```

## 文档（第5部分检查要点）

| 文档 | 内容 |
|------|------|
| [docs/UI_PROTOTYPE.md](docs/UI_PROTOTYPE.md) | 用户界面原型 |
| [docs/INTERACTION_DESIGN.md](docs/INTERACTION_DESIGN.md) | 交互设计原则 |
| [docs/STATIC_ANALYSIS.md](docs/STATIC_ANALYSIS.md) | 五类故障静态分析 |
| [docs/CLASS_DIAGRAM.md](docs/CLASS_DIAGRAM.md) | 类结构 UML |
| [docs/MENU_STATE_DIAGRAM.md](docs/MENU_STATE_DIAGRAM.md) | 菜单状态转换 UML |
| [docs/DESIGN.md](docs/DESIGN.md) | 整体设计（含第4部分） |
| [docs/FLOW.md](docs/FLOW.md) | 业务流程图 |

## 目录结构

```
main.py                 # 唯一 main() 入口
src/
  app.py                # Application 主循环
  menu.py               # 菜单导航
  handlers.py           # 华经理端功能
  interactive.py        # 小明交互练习
  io/console.py         # 控制台 I/O 抽象
  generator.py          # 出题（故事1~3）
  repository.py         # CSV 存储（故事4）
  ...
data/                   # CSV 与导出文件
docs/                   # 设计文档
tests/                  # 单元测试
```

## Git / Gitee 规范

```powershell
git add .
git commit -m "feat: 完成第5部分用户交互集成"
git remote add origin <你的gitee仓库地址>
git push -u origin main
```

- 提交信息：`feat:` / `fix:` / `docs:` + 简述
- 不提交 `venv/`、`__pycache__/`
