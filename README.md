# Script Project

## 專案結構

```
main.py
core/
    __init__.py
    recorder.py
utils/
    __init__.py
    admin_check.py
```

## 說明
- `main.py`：主程式入口。
- `core/`：核心功能模組。
  - `recorder.py`：錄製相關功能。
- `utils/`：工具模組。
  - `admin_check.py`：管理員檢查工具。

## 使用方式
1. 安裝 Python 3.12 或以上版本。
2. 執行主程式：
   ```powershell
   python main.py
   ```

## 範例

執行主程式後，依照提示操作：

- 按 `F2` 開始/停止錄製巨集。
- 按 `F9` 開始重播錄製內容。
- 按 `F10` 停止重播。

```python
from utils import run_as_admin
from core import MacroRecorder

def main():
    run_as_admin()
    print("巨集錄製程式已啟動")
    print("按 F2 開始/停止錄製")
    print("按 F9 開始重播")
    print("按 F10 停止重播")
    macro_recorder = MacroRecorder()
    macro_recorder.start()

if __name__ == "__main__":
    main()
```


