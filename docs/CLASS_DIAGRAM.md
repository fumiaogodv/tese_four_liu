# 类结构 UML 图

```mermaid
classDiagram
    direction TB

    class Application {
        -io: TextIO
        -navigator: MenuNavigator
        +run()
        -_dispatch(handler_name)
    }

    class MenuNavigator {
        -io: TextIO
        +state: MenuState
        +render_main_menu()
        +read_choice() str
        +transition(choice) tuple
    }

    class ConsoleIO {
        +prompt(message, default) str
        +println(message)
    }

    class TextIO {
        <<interface>>
        +prompt()
        +println()
    }

    class PracticeSession {
        +session_id: str
        +practice_date: str
        +practice_type: str
        +exercises: list
        +total: int
    }

    class ExerciseItem {
        +seq: int
        +expression: str
        +correct_answer: int
    }

    class StudentAnswer {
        +seq: int
        +expression: str
        +student_answer: int
    }

    class GradeResult {
        +session_id: str
        +total: int
        +correct: int
        +score: float
        +details: list
    }

    Application --> MenuNavigator
    Application --> TextIO
    ConsoleIO ..|> TextIO
    MenuNavigator --> TextIO

    Application ..> handlers : dispatch
    Application ..> interactive : dispatch

    note for handlers "华经理端命令\ncreate/export/import/..."

    note for interactive "小明交互练习\ncollect_answers + grade"

    PracticeSession *-- ExerciseItem
    GradeResult o-- GradeDetail

    handlers ..> generator
    handlers ..> repository
    handlers ..> grader
    handlers ..> analyzer
    interactive ..> generator
    interactive ..> grader
    interactive ..> repository

    repository ..> PracticeSession
    grader ..> GradeResult
    generator ..> PracticeSession
```

## 模块分层

| 层 | 模块 | 职责 |
|----|------|------|
| 入口 | `main.py` | 唯一 `main()` |
| 应用 | `app.Application` | 主循环、调度 |
| 交互 | `menu`, `io`, `handlers`, `interactive` | CLI 与用户输入 |
| 领域 | `generator`, `grader`, `analyzer`, `export` | 业务逻辑 |
| 数据 | `repository`, `models`, `parsers` | 持久化与解析 |
| 横切 | `contracts`, `exceptions`, `constants` | 契约、异常、配置 |
