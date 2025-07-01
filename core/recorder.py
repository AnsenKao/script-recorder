from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Controller as MouseController, Listener as MouseListener
import time
import threading

class MacroRecorder:
    def __init__(self):
        self.recorded_events = []
        self.is_recording = False
        self.is_playing = False
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()
        self.last_time = None
        
    def on_press(self, key):
        if key == keyboard.Key.f2:
            if not self.is_recording:
                print("開始錄製...")
                self.recorded_events = []
                self.is_recording = True
                self.last_time = time.time()
            else:
                print("停止錄製")
                self.is_recording = False
                self.display_recorded_events()
        elif key == keyboard.Key.f9:
            if not self.is_playing:
                print("開始重播...")
                self.is_playing = True
                threading.Thread(target=self.play_macro).start()
        elif key == keyboard.Key.f10:
            self.is_playing = False
            print("停止重播")
        elif self.is_recording:
            current_time = time.time()
            self.recorded_events.append(('key_press', key, current_time - self.last_time))
            self.last_time = current_time

    def on_release(self, key):
        if self.is_recording and key != keyboard.Key.f2:
            current_time = time.time()
            self.recorded_events.append(('key_release', key, current_time - self.last_time))
            self.last_time = current_time

    def on_click(self, _, __, button, pressed):
        if self.is_recording:
            current_time = time.time()
            event_type = 'mouse_press' if pressed else 'mouse_release'
            self.recorded_events.append((event_type, button, current_time - self.last_time))
            self.last_time = current_time

    def on_scroll(self, _, __, dx, dy):
        if self.is_recording:
            current_time = time.time()
            self.recorded_events.append(('mouse_scroll', (dx, dy), current_time - self.last_time))
            self.last_time = current_time

    def play_macro(self):
        while self.is_playing:
            for event in self.recorded_events:
                if not self.is_playing:
                    break

                time.sleep(0.05)
                event_type = event[0]
                data = event[1]

                try:
                    if event_type == 'key_press':
                        self.keyboard_controller.press(data)
                    elif event_type == 'key_release':
                        self.keyboard_controller.release(data)
                    elif event_type == 'mouse_press':
                        self.mouse_controller.press(data)
                    elif event_type == 'mouse_release':
                        self.mouse_controller.release(data)
                    elif event_type == 'mouse_scroll':
                        dx, dy = data
                        self.mouse_controller.scroll(dx, dy)
                except Exception as e:
                    print(f"執行動作時發生錯誤: {e}")
                    continue
            
            # time.sleep(3)

    def start(self):
        keyboard_listener = KeyboardListener(
            on_press=self.on_press,
            on_release=self.on_release)
        mouse_listener = MouseListener(
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        
        keyboard_listener.start()
        mouse_listener.start()
        
        keyboard_listener.join()
        mouse_listener.join()

    def display_recorded_events(self):
        print("\n錄製的操作記錄：")
        print("-" * 50)
        for i, event in enumerate(self.recorded_events, 1):
            event_type = event[0]
            data = event[1]
            
            if event_type.startswith('key'):
                try:
                    key_name = data.char if hasattr(data, 'char') else str(data)
                    action = "按下" if event_type == 'key_press' else "釋放"
                    print(f"{i}. 鍵盤{action}: {key_name}")
                except:
                    print(f"{i}. 鍵盤{action}: {str(data)}")
            elif event_type.startswith('mouse'):
                if event_type == 'mouse_scroll':
                    dx, dy = data
                    direction = "上" if dy > 0 else "下" if dy < 0 else "水平"
                    print(f"{i}. 滑鼠滾輪: {direction}")
                else:
                    action = "按下" if event_type == 'mouse_press' else "釋放"
                    print(f"{i}. 滑鼠{action}: {str(data)}")
        print("-" * 50)