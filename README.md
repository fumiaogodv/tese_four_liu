# 口算练习 · 数据处理（软件构造案例第4部分）

面向华经理场景：生成练习卷、CSV 存储、导入答案自动判题、成绩与错题分析。

## 环境

- Python 3.10+
- 使用项目内虚拟环境 `venv`

```powershell
cd c:\Users\godv\Desktop\vibe_coding\test_four_liu
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 运行

```powershell
python main.py
```

主菜单功能：

1. 生成练习卷（加法 / 减法 / 混合）→ `data/practices.csv` + 可打印 txt  
2. 导出已有练习卷  
3. 导入学生答案文本并判题 → `answers.csv`、`results.csv`  
4. 查看成绩列表  
5. 错题与按日汇总分析  
6. 查看单次练习详情  

## 文档

- [docs/DESIGN.md](docs/DESIGN.md) — 设计说明（数据建模、契约、正则、表驱动等）  
- [docs/FLOW.md](docs/FLOW.md) — 交互流程图（Mermaid）  

## 测试

```powershell
pytest tests/ -v
```

## 目录结构

```
main.py              # 入口
src/                 # 业务代码
data/                # CSV 与导出文件
docs/                # 设计文档与流程图
tests/               # 单元测试
```

## Git 规范建议

- 提交信息：`类型: 简述`（如 `feat: 增加错题统计`）  
- 不提交 `venv/`、`__pycache__/`、本地敏感数据  
