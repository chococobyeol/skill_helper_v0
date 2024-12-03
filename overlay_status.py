import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import threading
import keyboard

class StatusOverlay:
    def __init__(self, macro_controller):
        self.macro_controller = macro_controller
        self.is_active = True
        
        # tkinter 초기화는 메인 스레드에서
        self.root = None
        self.labels = {}
        
        # 초기화 완료 이벤트
        self.init_done = threading.Event()
        
    def initialize_gui(self):
        # 메인 윈도우 생성
        self.root = tk.Tk()
        self.root.title("매크로 상태")
        
        # 윈도우 설정
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.85)
        self.root.overrideredirect(True)
        
        # 윈도우 위치 설정
        self.root.geometry('180x230+10+50')
        
        # 프레임 생성
        frame = ttk.Frame(self.root, padding="5")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 스타일 설정
        style = ttk.Style()
        style.configure('Title.TLabel', font=('맑은 고딕', 10, 'bold'))
        style.configure('Status.TLabel', font=('맑은 고딕', 9))
        
        # 타이틀
        title = ttk.Label(frame, text="매크로 상태", style='Title.TLabel')
        title.pack(pady=(0, 5))
        
        # 구분선
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
        # 상태 표시 레이블들
        self.labels = {
            'skill1': ttk.Label(frame, text="F1: 비활성", style='Status.TLabel'),
            'skill2': ttk.Label(frame, text="F2: 비활성", style='Status.TLabel'),
            'skill3': ttk.Label(frame, text="F3: 비활성", style='Status.TLabel'),
            'skill4': ttk.Label(frame, text="F4: 비활성", style='Status.TLabel'),
            'skill4_party': ttk.Label(frame, text="F4파티: 비활성", style='Status.TLabel'),
            'skill9': ttk.Label(frame, text="F9: 비활성", style='Status.TLabel'),
            'heal': ttk.Label(frame, text="힐링: 활성", style='Status.TLabel')
        }
        
        # 레이블 배치
        for label in self.labels.values():
            label.pack(anchor='w', padx=10, pady=2)
        
        # 하단 구분선
        separator2 = ttk.Separator(frame, orient='horizontal')
        separator2.pack(fill='x', pady=5)
        
        # 종료 안내
        exit_label = ttk.Label(frame, text="Ctrl+Q: 종료", style='Status.TLabel', foreground='gray')
        exit_label.pack(anchor='e', padx=5)
        
        # 클릭해서 드래그 가능하도록
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        # Ctrl+Q 종료 이벤트 바인딩
        self.root.bind('<Control-q>', self.on_exit)
        
        # 초기화 완료
        self.init_done.set()
        
        # 상태 업데이트 시작
        self.update_status()
        
        # 메인루프 시작
        while self.is_active:
            try:
                self.root.update()
                self.root.update_idletasks()
                # Ctrl+Q 체크
                if keyboard.is_pressed('ctrl+q'):
                    self.on_exit()
                    break
            except:
                break

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_status(self):
        if not self.is_active:
            return
            
        # 매크로 상태 업데이트
        for key, label in self.labels.items():
            is_active = False
            if key == 'heal':
                is_active = self.macro_controller.heal_controller.is_running
            elif key == 'skill4_party':
                is_active = self.macro_controller.skill_macro_4.use_party_skill
                status = "활성" if is_active else "비활성"
                label.config(text=f"F4파티: {status}", foreground='#007ACC' if is_active else 'black')
                continue
            else:
                macro = getattr(self.macro_controller, f'skill_macro_{key[-1]}')
                is_active = macro.is_running
            
            status = "활성" if is_active else "비활성"
            color = '#007ACC' if is_active else 'black'
            label.config(text=f"{key.upper()}: {status}", foreground=color)
        
        # 100ms마다 업데이트
        if self.is_active:
            self.root.after(100, self.update_status)

    def run(self):
        self.initialize_gui()

    def stop(self):
        self.is_active = False
        if self.root:
            self.root.quit()

    def on_exit(self, event=None):
        self.is_active = False
        self.macro_controller.is_active = False
        if self.root:
            self.root.quit() 