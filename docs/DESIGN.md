# 口算练习数据处理 — 设计文档

对应课程案例 **第 4 部分：数据处理的软件构造**。

## 1. 业务背景

华经理每天选择加法/减法/加减混合练习卷，打印给小明纸上作答；家长将答案录入电脑后，程序读入练习与答案，**自动判题、打分、CSV 持久化**，并支持**按日成绩与错题频次分析**，便于针对性辅导。

## 2. 交互流程

见 [FLOW.md](./FLOW.md)（Mermaid 流程图）。

## 3. 数据建模

| 结构 | 说明 |
|------|------|
| `ExerciseItem` | 单题：序号、算式、标准答案 |
| `PracticeSession` | 一次练习卷：session_id、日期、类型、题目列表 |
| `StudentAnswer` | 学生单题答案 |
| `GradeResult` / `GradeDetail` | 判题汇总与明细 |
| `WrongStat` | 错题聚合统计 |

**CSV 文件（`data/` 目录）**

| 文件 | 用途 |
|------|------|
| `practices.csv` | 练习卷题目 |
| `answers.csv` | 学生答案 |
| `results.csv` | 每次判题成绩 |
| `wrong_stats.csv` | 错题累计 |

## 4. 表驱动编程

- `src/constants.py`：`MENU_ITEMS`、`PRACTICE_TYPE_*`、`GENERATION_RULES`、CSV 表头
- `src/generator.py`：`_GENERATORS` 映射练习类型 → 生成函数
- `src/app.py`：`_HANDLERS` 映射菜单 → 命令处理

扩展新练习类型或菜单项时，优先改表配置而非散落 `if/elif`。

## 5. 契约式编程

- `src/contracts.py`：`require`（前置）、`ensure`（后置）、`invariant`（不变量）
- 应用位置：解析算式、生成题量、判题数量一致、`GradeResult` 正确数不超过总题数

## 6. 字符串与正则

- `src/parsers.py`：
  - `EXPRESSION_PATTERN`：校验/解析 `48+7`、`15-6`
  - `ANSWER_LINE_PATTERN`：解析答案行 `48+7=55`
  - `SESSION_ID_PATTERN`：校验 `20260528_add` 形式 session_id

## 7. 防御性编程

- 自定义异常层次：`OralCalcError` → `ValidationError` / `StorageError` / `NotFoundError`
- CSV 读写捕获 `OSError`、`csv.Error` 转为 `StorageError`
- 导入答案：跳过空行/注释，非法行收集后一次性报错
- CLI 层统一捕获 `OralCalcError` 提示用户

## 8. 模块职责（单一职责）

| 模块 | 职责 |
|------|------|
| `models` | 数据结构 |
| `generator` | 出题 |
| `repository` | CSV 持久化 |
| `grader` | 判题 |
| `analyzer` | 统计展示 |
| `export` | 打印文本 |
| `app` | 交互菜单 |

## 9. 运行方式

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 10. 测试

```bash
pytest tests/ -v
```
