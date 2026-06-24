# GUI 设计原则（故事8 / 第7部分）

## 1. 一致性（Consistency）

- 左侧固定导航 + 右侧内容区，所有功能同一布局范式。
- 按钮、下拉框、标签使用统一 `ttk` 样式与「微软雅黑」字体。

## 2. 可见性（Visibility）

- 当前功能标题、进度（口算练习 `进度: 3/10`）、状态栏实时反馈。
- 华经理与小明功能在导航上标注角色。

## 3. 反馈（Feedback）

- 操作成功/失败使用 `messagebox` 与状态栏双通道反馈。
- 交互练习每题提交后更新题目与进度。

## 4. 容错（Forgiveness）

- 非法答案提示重输，不中断整场练习。
- 文件对话框避免手输长路径。

## 5. 简约（Simplicity）

- 鼠标点击完成类型选择、文件浏览、提交答案。
- 键盘仍支持回车提交答案（`Return` 事件）。

## 6. 可测试性（Testability）

- **GuiController** 不依赖 tkinter，业务逻辑用 pytest 覆盖。
- GUI 视图仅负责绑定事件与展示，符合 MVC 分离。

## 7. 事件驱动编程

| 事件类型 | 触发源 | 处理 |
|----------|--------|------|
| `Button` command | 侧边栏导航、生成、导出、判题 | 切换面板 / 调用 Controller |
| `Combobox` 选择 | 练习类型、练习卷 | 读取选项 |
| `<Return>` | 答案输入框 | 提交当前题 |
| `WM_DELETE_WINDOW` | 关闭窗口 | 退出程序 |
| `filedialog` | 浏览按钮 | 选择答案/导出路径 |

## 8. 观察者模式应用

| 观察者 | 订阅事件 | 作用 |
|--------|----------|------|
| `StatusBarObserver` | 所有带 message 的事件 | 更新底部状态栏 |
| `_SessionRefreshObserver` | `PRACTICE_CREATED`, `SESSION_LIST_CHANGED` | 刷新练习卷下拉列表 |
| `AppEventBus`（Subject） | Controller 发布 | 解耦 UI 与业务通知 |

实现位置：`src/gui/events.py`、`src/gui/panels.py`、`src/gui/main_window.py`。

## 9. 与 CLI 关系

- `python main.py` → GUI（默认）
- `python main.py --cli` → 原有命令行界面
