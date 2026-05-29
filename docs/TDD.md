# TDD 测试驱动开发

本项目采用 **pytest** 进行自动化测试。故事7 要求体现 TDD 思想，以下以 `SessionIdBuilder` 为例说明完整循环。

## TDD 三步循环

```
红 (Red)   → 先写失败测试，明确期望行为
绿 (Green) → 写最少代码使测试通过
重构 (Refactor) → 整理结构，保持测试通过
```

## 案例：同日多次练习的 session_id 去重

### 需求

同一天生成多套同类型练习时，`session_id` 不能冲突：

- 第一套：`20260528_add`
- 第二套：`20260528_add_2`
- 第三套：`20260528_add_3`

### 1. 红 — 先写测试

见 `tests/test_tdd_session_id.py`：

```python
def test_session_id_avoids_collision():
    builder = SessionIdBuilder()
    existing = {"20260528_add"}
    sid = builder.build("addition", date(2026, 5, 28), existing)
    assert sid == "20260528_add_2"
```

此时 `SessionIdBuilder` 尚未实现，测试失败。

### 2. 绿 — 实现类

见 `src/services/session_id.py`：

```python
class SessionIdBuilder:
    def build(self, practice_type, day=None, existing_ids=None) -> str:
        ...
```

运行 `pytest tests/test_tdd_session_id.py -v` 全部通过。

### 3. 重构 — 接入服务层

将原 `generator._session_id()` 内联逻辑移除，改为：

```python
self._session_ids.build(practice_type, today, set(self._repository.list_session_ids()))
```

回归测试：`pytest tests/ -v` 确保无破坏。

## 项目测试策略

| 层次 | 测试文件 | 说明 |
|------|----------|------|
| 解析/契约 | `test_parsers.py` | 算式、答案行 |
| 仓储 | `test_repository.py` | CSV 读写 |
| 服务 | `test_services.py` | 容器装配、判题持久化 |
| 命令 | `test_commands.py` | Command 模式 |
| 菜单/应用 | `test_menu.py` | CLI 导航 |
| 交互 | `test_interactive.py` | 逐题作答 |
| TDD 示例 | `test_tdd_session_id.py` | 红-绿-重构示范 |

## 运行测试

```powershell
.\venv\Scripts\python -m pytest tests/ -v
```

建议在每次重构后执行全量测试（回归），替代手工重复验证。
