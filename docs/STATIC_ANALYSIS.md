# 静态程序分析（故障类型）

对当前口算练习系统进行静态分析，按教程要求的五类故障逐项说明**风险点**与**已有防护**。

## 1. 数据故障（Data Faults）

| 风险 | 位置 | 防护措施 |
|------|------|----------|
| 算式格式非法 | `parsers.parse_expression` | 正则校验 + `ValidationError` |
| 加法结果 ≥100 / 减法差 <0 | `generator`, `parsers` | 生成约束 + `require` 契约 |
| CSV 字段缺失或类型错误 | `repository` | `DictReader` + 显式 `int()` 转换，损坏时 `StorageError` |
| 答案与题目数量不一致 | `grader.grade` | 前置条件 `require(len(answers)==total)` |
| session_id 重复覆盖 | `generator._session_id` | 自动追加 `_2`、`_3` 序号 |

## 2. 控制故障（Control Faults）

| 风险 | 位置 | 防护措施 |
|------|------|----------|
| 无效菜单选项 | `MenuNavigator.transition` | 返回 `None`，主循环提示重输 |
| 交互练习中途放弃 | `interactive.collect_answers` | 检测 `q`，抛出 `ValidationError` 安全退出 |
| 无限重试读整数 | `interactive._read_int_answer` | 循环直至合法输入（有界用户操作） |
| 主循环无法退出 | `Application.run` | 选项 0 → `MenuState.EXIT` |

## 3. 输入/输出故障（I/O Faults）

| 风险 | 位置 | 防护措施 |
|------|------|----------|
| 用户输入非数字 | `interactive`, `ConsoleIO` | try/except `ValueError`，提示重输 |
| 文件不存在 | `grader.parse_answers_from_file` | `require(path.exists())` |
| 文件编码/读取失败 | `repository`, `grader` | 捕获 `OSError` → `StorageError`/`ValidationError` |
| stdin EOF | `ConsoleIO.prompt` | 捕获 `EOFError`，返回默认值 |
| 控制台输出失败 | `ConsoleIO.println` | flush 后由系统异常向上传播，主循环捕获 |

## 4. 接口故障（Interface Faults）

| 风险 | 位置 | 防护措施 |
|------|------|----------|
| 菜单 handler 名与实现不匹配 | `constants.MAIN_MENU_ITEMS`, `handlers.HANDLERS` | 表驱动映射，单元测试校验菜单项 |
| 模块间数据结构不一致 | `models`  dataclass | 统一 `PracticeSession` / `StudentAnswer` 接口 |
| session_id 格式不统一 | `parsers.normalize_session_id` | 正则契约校验 |
| IO 接口替换失败 | `TextIO` Protocol + `ConsoleIO` | 测试用 `FakeIO` 注入 |

## 5. 存储管理故障（Storage Faults）

| 风险 | 位置 | 防护措施 |
|------|------|----------|
| data 目录不存在 | `repository._path` | `mkdir(parents=True, exist_ok=True)` |
| CSV 写入中断 | `repository._write_csv` | 整文件重写策略；异常转 `StorageError` |
| 并发写入冲突 | 当前单机 CLI | 未并发设计；文档说明单用户场景 |
| 读取空文件 | `repository._read_csv` | 返回空列表，上层 `NotFoundError` |
| 成绩/答案覆盖 | `save_*` 按 session_id 过滤后合并 | 同 session 重新判题覆盖旧记录 |

## 改进建议（后续迭代）

- 对 CSV 写入增加临时文件 + 原子替换，降低写入中断导致文件损坏的概率。
- 交互练习支持断点续做（持久化当前题号）。
