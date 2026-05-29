# 类结构 UML 图

```mermaid
classDiagram
    direction TB

    %% 使用更兼容的类名中文化语法
    class Application["应用程序 (Application)"]
    class MenuNavigator["菜单导航器 (MenuNavigator)"]
    class ConsoleIO["控制台输入输出 (ConsoleIO)"]
    class TextIO["文本输入输出接口 (TextIO)"]
    class PracticeSession["练习会话 (PracticeSession)"]
    class ExerciseItem["练习题目项 (ExerciseItem)"]
    class StudentAnswer["学生答案 (StudentAnswer)"]
    class GradeResult["批改成绩结果 (GradeResult)"]
    class GradeDetail["成绩详情明细 (GradeDetail)"]

    class Application {
        -输入输出对象: TextIO
        -菜单导航: MenuNavigator
        +运行启动() run
        -_分发调度(处理器名称) _dispatch
    }

    class MenuNavigator {
        -输入输出对象: TextIO
        +当前状态: MenuState
        +渲染主菜单()
        +读取用户选择() str
        +状态转换(选择) tuple
    }

    class ConsoleIO {
        +提示输入(消息, 默认值) str
        +打印换行(消息)
    }

    class TextIO {
        <<interface>>
        +提示输入()
        +打印换行()
    }

    class PracticeSession {
        +会话ID: str
        +练习日期: str
        +练习类型: str
        +题目列表: list
        +总题数: int
    }

    class ExerciseItem {
        +题号: int
        +算式表达式: str
        +正确答案: int
    }

    class StudentAnswer {
        +题号: int
        +算式表达式: str
        +学生所填答案: int
    }

    class GradeResult {
        +会话ID: str
        +总题数: int
        +答对题数: int
        +最终得分: float
        +批改详情: list
    }

    %% 关系连线
    Application --> MenuNavigator
    Application --> TextIO
    ConsoleIO ..|> TextIO
    MenuNavigator --> TextIO

    Application ..> 管理员业务处理器 : 分发调度
    Application ..> 学生交互业务 : 分发调度

    note for 管理员业务处理器 "【华经理端命令】\n批量生成/挑选导出/导入批改/..."
    note for 学生交互业务 "【小明交互练习】\n收集答案 + 自动批改"

    PracticeSession *-- ExerciseItem
    GradeResult o-- GradeDetail

    管理员业务处理器 ..> 题目生成器
    管理员业务处理器 ..> 数据仓库
    管理员业务处理器 ..> 批改器
    管理员业务处理器 ..> 错题分析器
    学生交互业务 ..> 题目生成器
    学生交互业务 ..> 批改器
    学生交互业务 ..> 数据仓库

    数据仓库 ..> PracticeSession
    批改器 ..> GradeResult
    题目生成器 ..> PracticeSession
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
