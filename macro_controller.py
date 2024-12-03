import time
import win32api
import win32con
from threading import Thread
import keyboard
import ctypes, sys
from healing_recovery import HealingController
from skills.skill_macro_1 import SkillMacro1Controller
from skills.skill_macro_2 import SkillMacro2Controller
from skills.skill_macro_3 import SkillMacro3Controller
from skills.skill_macro_4 import SkillMacro4Controller
from skills.skill_macro_9 import SkillMacro9Controller
from overlay_status import StatusOverlay

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MacroController:
    def __init__(self):
        self.is_active = True
        self.EXIT_KEY = 'ctrl+q'
        self.is_using_skill = False
        self.current_skill = None  # 현재 실행 중인 스킬 표시
        
        # 컨트롤러 초기화
        self.heal_controller = HealingController()
        self.heal_controller.macro_controller = self  # 매크로 컨트롤러 참조 추가
        
        self.skill_macro_1 = SkillMacro1Controller()
        self.skill_macro_2 = SkillMacro2Controller()
        self.skill_macro_3 = SkillMacro3Controller()
        self.skill_macro_4 = SkillMacro4Controller()
        self.skill_macro_9 = SkillMacro9Controller()
        self.skill_macro_9.macro_controller = self  # 매크로 컨트롤러 참조 설정
        
        # 힐링은 기본적으로 활성화
        self.heal_controller.is_running = True
        
        # 단축키 설정
        self.setup_hotkeys()

    def setup_hotkeys(self):
        keyboard.on_press_key('F1', lambda _: self.toggle_skill_macro_1())
        keyboard.on_press_key('F2', lambda _: self.toggle_skill_macro_2())
        keyboard.on_press_key('F3', lambda _: self.toggle_skill_macro_3())
        keyboard.on_press_key('F4', lambda _: self.toggle_skill_macro_4())
        keyboard.on_press_key('F9', lambda _: self.toggle_skill_macro_9())

    def toggle_skill_macro_1(self):
        self.skill_macro_1.is_running = not self.skill_macro_1.is_running
        status = "실행 중" if self.skill_macro_1.is_running else "정지"
        print(f"\n스킬 매크로 1 상태: {status}")

    def toggle_skill_macro_2(self):
        self.skill_macro_2.is_running = not self.skill_macro_2.is_running
        status = "실행 중" if self.skill_macro_2.is_running else "정지"
        print(f"\n스킬 매크로 2 상태: {status}")

    def toggle_skill_macro_3(self):
        self.skill_macro_3.is_running = not self.skill_macro_3.is_running
        status = "실행 중" if self.skill_macro_3.is_running else "정지"
        print(f"\n스킬 매크로 3 상태: {status}")

    def toggle_skill_macro_4(self):
        self.skill_macro_4.is_running = not self.skill_macro_4.is_running
        status = "실행 중" if self.skill_macro_4.is_running else "정지"
        print(f"\n스킬 매크로 4 상태: {status}")

    def toggle_skill_macro_9(self):
        self.skill_macro_9.is_running = not self.skill_macro_9.is_running
        status = "실행 중" if self.skill_macro_9.is_running else "정지"
        print(f"\n몹 킬러 매크로 상태: {status}")

    def run_skill_macro_1(self):
        while self.is_active:
            try:
                # 다른 스킬이 실행 중이면 대기
                if self.is_using_skill and self.current_skill != "skill1":
                    time.sleep(0.01)
                    continue

                # 힐/마나 체크
                if (self.heal_controller.is_healing or 
                    self.heal_controller.mana_controller.is_recovering):
                    time.sleep(0.01)
                    continue

                # 스킬 사용
                if self.skill_macro_1.is_running:
                    self.is_using_skill = True
                    self.current_skill = "skill1"
                    self.skill_macro_1.use_skill()
                    self.is_using_skill = False
                    self.current_skill = None

                time.sleep(0.01)

            except Exception as e:
                print(f"매크로 실행 중 오류: {str(e)}")
                self.is_using_skill = False
                self.current_skill = None

    def run_skill_macro_2(self):
        while self.is_active:
            try:
                # 다른 스킬이 실행 중이면 대기
                if self.is_using_skill and self.current_skill != "skill2":
                    time.sleep(0.01)
                    continue

                # 힐/마나 체크
                if (self.heal_controller.is_healing or 
                    self.heal_controller.mana_controller.is_recovering):
                    time.sleep(0.01)
                    continue

                # 스킬 사용
                if self.skill_macro_2.is_running:
                    self.is_using_skill = True
                    self.current_skill = "skill2"
                    self.skill_macro_2.use_skill()
                    self.is_using_skill = False
                    self.current_skill = None

                time.sleep(0.01)

            except Exception as e:
                print(f"매크로 실행 중 오류: {str(e)}")
                self.is_using_skill = False
                self.current_skill = None

    def run_skill_macro_3(self):
        while self.is_active:
            try:
                # 다른 스킬이 실행 중이면 대기
                if self.is_using_skill and self.current_skill != "skill3":
                    time.sleep(0.01)
                    continue

                # 힐/마나 체크
                if (self.heal_controller.is_healing or 
                    self.heal_controller.mana_controller.is_recovering):
                    time.sleep(0.01)
                    continue

                # 스킬 사용
                if self.skill_macro_3.is_running:
                    self.is_using_skill = True
                    self.current_skill = "skill3"
                    self.skill_macro_3.use_skill()
                    self.is_using_skill = False
                    self.current_skill = None

                time.sleep(0.01)

            except Exception as e:
                print(f"매크로 실행 중 오류: {str(e)}")
                self.is_using_skill = False
                self.current_skill = None

    def run_skill_macro_4(self):
        while self.is_active:
            try:
                # 다른 스킬이 실행 중이면 대기
                if self.is_using_skill and self.current_skill != "skill4":
                    time.sleep(0.01)
                    continue

                # 힐/마나 체크
                if (self.heal_controller.is_healing or 
                    self.heal_controller.mana_controller.is_recovering):
                    time.sleep(0.01)
                    continue

                # 스킬 사용
                if self.skill_macro_4.is_running:
                    self.is_using_skill = True
                    self.current_skill = "skill4"
                    self.skill_macro_4.use_skill()
                    self.is_using_skill = False
                    self.current_skill = None

                time.sleep(0.01)

            except Exception as e:
                print(f"매크로 실행 중 오류: {str(e)}")
                self.is_using_skill = False
                self.current_skill = None

    def run_skill_macro_9(self):
        while self.is_active:
            try:
                # 스킬 사용
                if self.skill_macro_9.is_running:
                    # 힐/마나 체크를 먼저
                    if (self.heal_controller.is_healing or 
                        self.heal_controller.mana_controller.is_recovering):
                        print("힐/마나 회복 대기...")
                        time.sleep(0.1)
                        continue

                    # 다른 스킬이 실행 중이면 대기
                    if self.is_using_skill and self.current_skill != "skill9":
                        time.sleep(0.01)
                        continue

                    self.is_using_skill = True
                    self.current_skill = "skill9"
                    
                    # 한 번의 시도만 실행
                    result = self.skill_macro_9.try_once()
                    if not result:  # 실패하면
                        self.skill_macro_9.fail_count += 1
                        if self.skill_macro_9.fail_count >= self.skill_macro_9.MAX_FAILS:
                            print(f"\n{self.skill_macro_9.MAX_FAILS}회 실패로 매크로 중지")
                            self.skill_macro_9.is_running = False
                            self.skill_macro_9.fail_count = 0
                    else:  # 성공하면
                        self.skill_macro_9.fail_count = 0

                    self.is_using_skill = False
                    self.current_skill = None

                time.sleep(0.01)

            except Exception as e:
                print(f"매크로 실행 중 오류: {str(e)}")
                self.is_using_skill = False
                self.current_skill = None

def main():
    # 관리자 권한 체크 및 요청
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    controller = MacroController()
    
    # 오버레이 창 생성
    overlay = StatusOverlay(controller)
    
    # 스레드 시작 (check_key_state 제외)
    threads = [
        Thread(target=controller.heal_controller.check_and_heal),
        Thread(target=controller.run_skill_macro_1),
        Thread(target=controller.run_skill_macro_2),
        Thread(target=controller.run_skill_macro_3),
        Thread(target=controller.run_skill_macro_4),
        Thread(target=controller.run_skill_macro_9),
    ]
    
    for thread in threads:
        thread.daemon = True
        thread.start()
    
    # 오버레이 실행
    try:
        overlay.run()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n프로그램 종료")
        controller.is_active = False
        overlay.stop()

if __name__ == "__main__":
    main() 