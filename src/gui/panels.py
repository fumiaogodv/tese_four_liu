"""GUI 面板组件。"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Callable

from src.gui.controller import GuiController
from src.gui.events import AppEvent, AppEventType, Observer


class StatusBarObserver:
    """观察者：将事件同步到状态栏。"""

    def __init__(self, set_status: Callable[[str], None]) -> None:
        self._set_status = set_status

    def on_event(self, event: AppEvent) -> None:
        if event.message:
            self._set_status(event.message)


class BasePanel(ttk.Frame):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, padding=12)
        self.controller = controller


class GeneratePanel(BasePanel):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(self, text="批量生成练习题", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor="w"
        )
        ttk.Label(self, text="选择练习类型后点击生成（自动保存 CSV 并导出打印文件）").pack(
            anchor="w", pady=(4, 12)
        )
        row = ttk.Frame(self)
        row.pack(fill="x")
        ttk.Label(row, text="练习类型:").pack(side="left")
        self._type = ttk.Combobox(
            row,
            state="readonly",
            values=[label for _, label in controller.practice_type_choices()],
            width=20,
        )
        self._type.current(0)
        self._type.pack(side="left", padx=8)
        ttk.Button(row, text="生成练习卷", command=self._on_generate).pack(side="left")
        self._output = scrolledtext.ScrolledText(self, height=12, font=("Consolas", 10))
        self._output.pack(fill="both", expand=True, pady=(12, 0))

    def _on_generate(self) -> None:
        idx = self._type.current()
        ptype = self.controller.practice_type_choices()[idx][0]
        try:
            session = self.controller.create_practice(ptype)
            lines = [
                f"session_id: {session.session_id}",
                f"类型: {self.controller.display_type_name(session.practice_type)}",
                f"题量: {session.total}",
                f"导出目录: {self.controller.data_dir / 'export'}",
            ]
            self._output.delete("1.0", tk.END)
            self._output.insert(tk.END, "\n".join(lines))
        except Exception as e:
            messagebox.showerror("错误", str(e))


class ExportPanel(BasePanel):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(self, text="挑选并导出练习卷", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor="w"
        )
        row = ttk.Frame(self)
        row.pack(fill="x", pady=12)
        ttk.Label(row, text="练习卷:").pack(side="left")
        self._sessions = ttk.Combobox(row, width=40, state="readonly")
        self._sessions.pack(side="left", padx=8)
        ttk.Button(row, text="刷新列表", command=self.refresh_sessions).pack(side="left", padx=4)
        ttk.Button(row, text="导出到文件", command=self._on_export).pack(side="left")

    def refresh_sessions(self) -> None:
        ids = self.controller.list_sessions()
        self._sessions["values"] = ids
        if ids:
            self._sessions.current(0)

    def _on_export(self) -> None:
        sid = self._sessions.get()
        if not sid:
            messagebox.showwarning("提示", "请先选择或生成练习卷")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{sid}_练习.txt",
            filetypes=[("文本文件", "*.txt")],
        )
        if not path:
            return
        try:
            out = self.controller.export_practice(sid, path)
            messagebox.showinfo("成功", f"已导出到 {out}")
        except Exception as e:
            messagebox.showerror("错误", str(e))


class ImportPanel(BasePanel):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(self, text="导入答案并批改", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor="w"
        )
        row1 = ttk.Frame(self)
        row1.pack(fill="x", pady=8)
        ttk.Label(row1, text="练习卷:").pack(side="left")
        self._sessions = ttk.Combobox(row1, width=40, state="readonly")
        self._sessions.pack(side="left", padx=8)
        ttk.Button(row1, text="刷新", command=self.refresh_sessions).pack(side="left")
        row2 = ttk.Frame(self)
        row2.pack(fill="x", pady=8)
        ttk.Label(row2, text="答案文件:").pack(side="left")
        self._path = ttk.Entry(row2, width=50)
        self._path.pack(side="left", padx=8)
        ttk.Button(row2, text="浏览...", command=self._browse).pack(side="left")
        ttk.Button(self, text="导入并判题", command=self._on_import).pack(anchor="w", pady=8)
        self._result = scrolledtext.ScrolledText(self, height=10, font=("Consolas", 10))
        self._result.pack(fill="both", expand=True)

    def refresh_sessions(self) -> None:
        ids = self.controller.list_sessions()
        self._sessions["values"] = ids
        if ids:
            self._sessions.current(0)

    def _browse(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if path:
            self._path.delete(0, tk.END)
            self._path.insert(0, path)

    def _on_import(self) -> None:
        sid = self._sessions.get()
        path = self._path.get().strip()
        if not sid or not path:
            messagebox.showwarning("提示", "请选择练习卷和答案文件")
            return
        try:
            result = self.controller.import_and_grade(sid, path)
            text = (
                f"得分: {result.score}\n"
                f"正确: {result.correct}/{result.total}\n"
            )
            if result.wrong_expressions:
                text += f"错题: {', '.join(result.wrong_expressions)}"
            self._result.delete("1.0", tk.END)
            self._result.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("错误", str(e))


class ResultsPanel(BasePanel):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(self, text="练习成绩统计", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor="w"
        )
        ttk.Button(self, text="刷新", command=self.refresh).pack(anchor="w", pady=8)
        self._text = scrolledtext.ScrolledText(self, height=16, font=("Consolas", 10))
        self._text.pack(fill="both", expand=True)

    def refresh(self) -> None:
        self._text.delete("1.0", tk.END)
        self._text.insert(tk.END, self.controller.get_results_text())


class AnalyzePanel(BasePanel):
    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(self, text="错题与薄弱题目分析", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor="w"
        )
        ttk.Button(self, text="刷新分析", command=self.refresh).pack(anchor="w", pady=8)
        self._text = scrolledtext.ScrolledText(self, height=16, font=("Consolas", 10))
        self._text.pack(fill="both", expand=True)

    def refresh(self) -> None:
        self._text.delete("1.0", tk.END)
        self._text.insert(tk.END, self.controller.get_analyze_text())


class PracticePanel(BasePanel):
    """小明交互式口算练习面板。"""

    def __init__(self, master: tk.Misc, controller: GuiController) -> None:
        super().__init__(master, controller)
        ttk.Label(
            self, text="交互式口算练习（小明）", font=("Microsoft YaHei UI", 14, "bold")
        ).pack(anchor="w")
        mode = ttk.LabelFrame(self, text="开始方式", padding=8)
        mode.pack(fill="x", pady=8)
        self._mode = tk.StringVar(value="new")
        ttk.Radiobutton(mode, text="新练习", variable=self._mode, value="new").pack(side="left")
        ttk.Radiobutton(mode, text="已有练习卷", variable=self._mode, value="existing").pack(
            side="left", padx=12
        )
        opts = ttk.Frame(self)
        opts.pack(fill="x", pady=4)
        ttk.Label(opts, text="类型:").pack(side="left")
        self._type = ttk.Combobox(
            opts,
            state="readonly",
            values=[label for _, label in controller.practice_type_choices()],
            width=16,
        )
        self._type.current(2)
        self._type.pack(side="left", padx=4)
        ttk.Label(opts, text="题量:").pack(side="left", padx=(12, 0))
        self._count = ttk.Spinbox(opts, from_=5, to=50, width=6)
        self._count.set("10")
        self._count.pack(side="left", padx=4)
        ttk.Label(opts, text="练习卷:").pack(side="left", padx=(12, 0))
        self._sessions = ttk.Combobox(opts, width=22, state="readonly")
        self._sessions.pack(side="left", padx=4)
        ttk.Button(opts, text="开始练习", command=self._on_start).pack(side="left", padx=12)

        quiz = ttk.LabelFrame(self, text="答题区", padding=16)
        quiz.pack(fill="both", expand=True, pady=8)
        self._progress = ttk.Label(quiz, text="进度: -", font=("Microsoft YaHei UI", 11))
        self._progress.pack(anchor="w")
        self._question = ttk.Label(
            quiz, text="请点击「开始练习」", font=("Microsoft YaHei UI", 28, "bold")
        )
        self._question.pack(pady=20)
        ans_row = ttk.Frame(quiz)
        ans_row.pack()
        ttk.Label(ans_row, text="你的答案:", font=("Microsoft YaHei UI", 12)).pack(side="left")
        self._answer = ttk.Entry(ans_row, width=12, font=("Microsoft YaHei UI", 14))
        self._answer.pack(side="left", padx=8)
        self._answer.bind("<Return>", lambda e: self._on_submit())
        ttk.Button(ans_row, text="提交", command=self._on_submit).pack(side="left")
        self._feedback = ttk.Label(quiz, text="", foreground="#0066cc")
        self._feedback.pack(pady=8)
        self._summary = scrolledtext.ScrolledText(quiz, height=6, font=("Consolas", 10))
        self._summary.pack(fill="both", expand=True)

    def refresh_sessions(self) -> None:
        ids = self.controller.list_sessions()
        self._sessions["values"] = ids
        if ids:
            self._sessions.current(0)

    def _on_start(self) -> None:
        try:
            if self._mode.get() == "existing":
                sid = self._sessions.get()
                if not sid:
                    messagebox.showwarning("提示", "请选择练习卷")
                    return
                self.controller.interactive_load(sid)
            else:
                idx = self._type.current()
                ptype = self.controller.practice_type_choices()[idx][0]
                count = int(self._count.get())
                self.controller.interactive_start_new(ptype, count)
            self._summary.delete("1.0", tk.END)
            self._show_current()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _show_current(self) -> None:
        ex = self.controller.interactive_current()
        cur, total = self.controller.interactive_progress()
        if ex is None:
            self._question.config(text="练习已完成")
            self._progress.config(text=f"进度: {total}/{total}")
            return
        self._progress.config(text=f"进度: {cur + 1}/{total}")
        self._question.config(text=f"{ex.expression} = ?")
        self._answer.delete(0, tk.END)
        self._answer.focus_set()

    def _on_submit(self) -> None:
        if not self.controller.interactive_is_active():
            messagebox.showinfo("提示", "请先开始练习")
            return
        try:
            result = self.controller.interactive_submit_answer(self._answer.get())
            if not result.accepted:
                self._feedback.config(text=result.message, foreground="#cc0000")
                return
            self._feedback.config(text=result.message, foreground="#0066cc")
            if result.is_complete and result.grade_result:
                gr = result.grade_result
                lines = [
                    f"得分: {gr.score}  ({gr.correct}/{gr.total})",
                ]
                for d in gr.details:
                    if not d.is_correct:
                        lines.append(
                            f"  {d.expression} = {d.student_answer} (正确 {d.correct_answer})"
                        )
                self._summary.delete("1.0", tk.END)
                self._summary.insert(tk.END, "\n".join(lines))
                self._question.config(text="恭喜完成！")
            else:
                self._show_current()
        except Exception as e:
            messagebox.showerror("错误", str(e))
