import time
import win32api
import win32con
import pyautogui
import keyboard
import os
from threading import Thread
from mana_recovery import ManaRecoveryController

class HealingController:
    def __init__(self):
        self.is_running = True
        self.is_active = True
        self.is_healing = False
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = False
        
        # 마나 회복 컨트롤러 초기화
        self.mana_controller = ManaRecoveryController()
        self.mana_controller.is_running = True  # 마나 회복은 항상 활성화
        
        # 이미지 파일 경로 설정
        self.img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
        self.lack_health_path = os.path.join(self.img_dir, 'lack_health.PNG')
        
        # 키 설정
        self.HEAL_KEY = 0x35  # 5키
        self.HOME_KEY = win32con.VK_HOME  # Home키
        self.ESC_KEY = win32con.VK_ESCAPE  # ESC키
        self.ENTER_KEY = win32con.VK_RETURN  # Enter키
        self.TOGGLE_KEY = 'F8'  # 매크로 토글 키
        self.EXIT_KEY = 'ctrl+q'  # 종료 키
        
        self.is_using_skill = False  # 스킬 사용 중 플래그 추가
        
        self.check_image_files()

    def check_image_files(self):
        if not os.path.exists(self.lack_health_path):
            print("\n=== 이미지 파일 확인 필요 ===")
            print(f"파일이 없습니다: {self.lack_health_path}")
            print("현재 작업 디렉토리:", os.getcwd())
            print("이미지 디렉토리:", self.img_dir)
            print("=========================\n")

    def send_key(self, key):
        win32api.keybd_event(key, 0, 0, 0)
        time.sleep(0.02)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.02)

    def find_image(self, image_path):
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                grayscale=True,
                region=(1285, 900, 235, 40)  # (1285, 900)~(1520, 940) 영역
            )
            if location:
                print(f"체력 부족 감지: {location}")
                return True
            return False
        except Exception as e:
            if not isinstance(e, pyautogui.ImageNotFoundException):
                print(f"오류 발생: {str(e)}")
            return False

    def use_heal_skill(self):
        if self.macro_controller.is_using_skill and self.macro_controller.current_skill != "heal":
            return

        self.is_using_skill = True
        self.macro_controller.is_using_skill = True
        self.macro_controller.current_skill = "heal"
        print("힐링 스킬 시도")
        
        try:
            keyboard.block_key('up')
            keyboard.block_key('down')
            keyboard.block_key('left')
            keyboard.block_key('right')
            keyboard.block_key('enter')
            
            self.send_key(self.ESC_KEY)
            time.sleep(0.01)
            self.send_key(self.HEAL_KEY)
            time.sleep(0.01)
            self.send_key(self.HOME_KEY)
            time.sleep(0.01)
            self.send_key(self.ENTER_KEY)
            time.sleep(0.01)
        
        finally:
            keyboard.unblock_key('up')
            keyboard.unblock_key('down')
            keyboard.unblock_key('left')
            keyboard.unblock_key('right')
            keyboard.unblock_key('enter')
            
            self.is_using_skill = False
            self.macro_controller.is_using_skill = False
            self.macro_controller.current_skill = None

    def check_and_heal(self):
        # 마나 회복 스레드 시작 - 이 부분을 다시 추가
        mana_thread = Thread(target=self.mana_controller.check_and_recover_mana)
        mana_thread.daemon = True
        mana_thread.start()

        while self.is_active:
            if self.is_running:
                try:
                    # 마나 회복 중이면 힐링 시도하지 않음
                    if self.mana_controller.is_recovering:
                        time.sleep(0.01)
                        continue

                    # 체력 부족 상태 체크
                    if self.find_image(self.lack_health_path):
                        self.is_healing = True
                        print("힐링 스킬 시도")
                        self.use_heal_skill()
                        time.sleep(0.05)
                    else:
                        self.is_healing = False

                except Exception as e:
                    print(f"매크로 실행 중 오류: {str(e)}")
                    self.is_healing = False
                
                time.sleep(0.01)
            time.sleep(0.01)

    def toggle_macro(self):
        self.is_running = not self.is_running
        status = "실행 중" if self.is_running else "정지"
        print(f"\n힐링 매크로 상태: {status}")

def main():
    controller = HealingController()
    
    macro_thread = Thread(target=controller.check_and_heal)
    macro_thread.daemon = True
    macro_thread.start()
    
    print("\n=== 힐링 매크로 시작 ===")
    print(f"{controller.TOGGLE_KEY}: 힐링 매크로 시작/정지")
    print(f"{controller.EXIT_KEY}: 프로그램 종료")
    
    keyboard.add_hotkey(controller.TOGGLE_KEY, controller.toggle_macro)
    
    try:
        keyboard.wait(controller.EXIT_KEY)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n프로그램 종료")
        controller.is_active = False

if __name__ == "__main__":
    main() 