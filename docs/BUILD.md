# 打包为可执行程序（故事7）

```powershell
cd c:\Users\godv\Desktop\vibe_coding\test_four_liu
.\venv\Scripts\Activate.ps1
pip install -r requirements-build.txt
.\scripts\build.ps1
```

输出：`dist\口算练习系统.exe`

## 在新机器上使用

1. 复制 `dist\口算练习系统.exe` 到任意目录  
2. 双击运行（无需安装 Python）  
3. 首次运行会在 exe 同目录自动创建 `data\` 文件夹存放 CSV  

## 说明

- 打包采用 **PyInstaller --onefile** 单文件模式  
- `data/samples` 作为模板随包分发；用户数据写入 exe 旁 `data/`  
- 开发模式仍使用 `python main.py`
