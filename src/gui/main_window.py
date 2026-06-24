"""tkinter 主窗口：事件驱动 GUI 入口。"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.container import get_container
from src.gui.controller import GuiController
from src.gui.events import AppEvent, AppEventBus, AppEventType
from src.gui.panels import (
    AnalyzePanel,
    ExportPanel,
    GeneratePanel,
    ImportPanel,
    PracticePanel,
    ResultsPanel,
    StatusBarObserver,
)


class MainWindow:
    """主窗口：侧边栏导航 + 内容区 + 状态栏。"""

    NAV_ITEMS = [
        ("generate", "批量生成", "华经理"),
        ("export", "导出练习", "华经理"),
        ("import", "导入批改", "华经理"),
        ("results", "成绩统计", "华经理"),
        ("analyze", "错题分析", "华经理"),
        ("practice", "口算练习", "小明"),
    ]

    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("口算练习系统")
        self._root.minsize(820, 560)
        self._root.configure(bg="#f0f4f8")

        self._bus = AppEventBus()
        self._controller = GuiController(get_container(), self._bus)

        self._setup_style()
        self._build_layout()
        self._bus.subscribe(StatusBarObserver(self._set_status))
        self._controller.event_bus.subscribe(
            _SessionRefreshObserver(self._panels_need_session_list)
        )
        self._show_panel("generate")
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_style(self) -> None:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Nav.TButton", padding=(12, 8), font=("Microsoft YaHei UI", 10))
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 16, "bold"), background="#2c5282", foreground="white")
        style.configure("Status.TLabel", font=("Microsoft YaHei UI", 9))

    def _build_layout(self) -> None:
        header = tk.Frame(self._root, bg="#2c5282", height=48)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="口算练习系统",
            font=("Microsoft YaHei UI", 16, "bold"),
            bg="#2c5282",
            fg="white",
        ).pack(side="left", padx=16, pady=8)
        tk.Label(
            header,
            text="GUI 图形界面 · 鼠标操作",
            font=("Microsoft YaHei UI", 10),
            bg="#2c5282",
            fg="#a0c4ff",
        ).pack(side="left")

        body = ttk.Frame(self._root)
        body.pack(fill="both", expand=True, padx=8, pady=8)

        nav = ttk.LabelFrame(body, text="功能菜单", padding=8)
        nav.pack(side="left", fill="y", padx=(0, 8))
        self._nav_buttons: dict[str, ttk.Button] = {}
        for key, title, role in self.NAV_ITEMS:
            btn = ttk.Button(
                nav,
                text=f"{title}\n({role})",
                style="Nav.TButton",
                command=lambda k=key: self._on_nav_click(k),
                width=14,
            )
            btn.pack(fill="x", pady=4)
            self._nav_buttons[key] = btn

        self._content = ttk.Frame(body)
        self._content.pack(side="left", fill="both", expand=True)

        self._panels: dict[str, ttk.Frame] = {
            "generate": GeneratePanel(self._content, self._controller),
            "export": ExportPanel(self._content, self._controller),
            "import": ImportPanel(self._content, self._controller),
            "results": ResultsPanel(self._content, self._controller),
            "analyze": AnalyzePanel(self._content, self._controller),
            "practice": PracticePanel(self._content, self._controller),
        }

        status_frame = ttk.Frame(self._root)
        status_frame.pack(fill="x", side="bottom")
        self._status = ttk.Label(
            status_frame,
            text="就绪",
            style="Status.TLabel",
            anchor="w",
            padding=(12, 6),
        )
        self._status.pack(fill="x")

    def _set_status(self, text: str) -> None:
        self._status.config(text=text)

    def _on_nav_click(self, key: str) -> None:
        """侧边栏按钮点击事件。"""
        self._show_panel(key)
        self._controller.event_bus.notify(AppEvent(AppEventType.PANEL_CHANGED, f"切换到 {key}"))

    def _show_panel(self, key: str) -> None:
        for k, panel in self._panels.items():
            panel.pack_forget()
        panel = self._panels[key]
        panel.pack(fill="both", expand=True)
        if key in ("export", "import", "practice") and hasattr(panel, "refresh_sessions"):
            panel.refresh_sessions()
        if key == "results" and hasattr(panel, "refresh"):
            panel.refresh()
        if key == "analyze" and hasattr(panel, "refresh"):
            panel.refresh()

    def _panels_need_session_list(self) -> None:
        for key in ("export", "import", "practice"):
            panel = self._panels.get(key)
            if panel and hasattr(panel, "refresh_sessions"):
                panel.refresh_sessions()

    def _on_close(self) -> None:
        """窗口关闭事件。"""
        self._root.destroy()

    def run(self) -> None:
        self._root.mainloop()


class _SessionRefreshObserver:
    """观察者：练习卷列表变化时刷新下拉框。"""

    def __init__(self, callback) -> None:
        self._callback = callback

    def on_event(self, event) -> None:
        if event.type in (
            AppEventType.PRACTICE_CREATED,
            AppEventType.SESSION_LIST_CHANGED,
        ):
            self._callback()


def run_gui() -> None:
    MainWindow().run()
