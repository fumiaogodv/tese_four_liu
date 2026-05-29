# 菜单状态转换 UML 图

```mermaid
stateDiagram-v2
    [*] --> MainMenu : 启动 main()

    MainMenu --> MainMenu : 无效输入 / 功能执行完毕
    MainMenu --> Exit : 输入 0

    state MainMenu {
        [*] --> Display
        Display --> WaitInput : 渲染菜单
        WaitInput --> Dispatch : 有效选项 1~6
        WaitInput --> Display : 无效选项
    }

    state Dispatch {
        [*] --> ManagerCmd : 选项 1~5
        [*] --> StudentCmd : 选项 6

        state ManagerCmd {
            [*] --> CreatePractice : 1 批量生成
            [*] --> ExportPractice : 2 挑选导出
            [*] --> ImportGrade : 3 导入批改
            [*] --> ListResults : 4 成绩统计
            [*] --> AnalyzeWrong : 5 错题分析
            CreatePractice --> [*]
            ExportPractice --> [*]
            ImportGrade --> [*]
            ListResults --> [*]
            AnalyzeWrong --> [*]
        }

        state StudentCmd {
            [*] --> ChooseMode : 新练习 / 已有卷
            ChooseMode --> Answering : 加载题目
            Answering --> Answering : 逐题输入
            Answering --> ShowScore : 全部答完
            Answering --> MainMenu : 输入 q 取消
            ShowScore --> [*] : 保存成绩
        }

        ManagerCmd --> MainMenu : 完成
        StudentCmd --> MainMenu : 完成
    }

    Exit --> [*] : 再见
```

## 状态说明

| 状态 | 说明 |
|------|------|
| `MainMenu` | 默认状态，循环显示图 5.1 菜单 |
| `ManagerCmd` | 华经理功能子流程，执行后返回主菜单 |
| `StudentCmd` | 小明交互练习子流程 |
| `Exit` | 用户选择 0，程序结束 |

## 实现对应

- `MenuState.MAIN` / `MenuState.EXIT` 定义于 `src/menu.py`
- `Application.run()` 实现 MainMenu ↔ Dispatch 循环
- `run_interactive_practice()` 实现 StudentCmd 子状态机
