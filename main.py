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