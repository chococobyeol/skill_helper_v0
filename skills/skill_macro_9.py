import time
import win32api
import win32con
import keyboard
import pyautogui
import os

class SkillMacro9Controller:
    def __init__(self):
        self.is_active = True
        self.is_running = False
        self.fail_count = 0
        self.MAX_FAILS = 10  # 최대 실패 횟수
        self.MAX_KILL_ATTEMPTS = 100  # 킬 시도 최대 횟수를 100으로 증가
        self.macro_controller = None  # 매크로 컨트롤러 참조 추가
        
        # 키 설정
        self.SKILL_KEY = 0x36  # 6키
        self.ENTER_KEY = win32con.VK_RETURN
        self.UP_KEY = win32con.VK_UP
        self.TOGGLE_KEY = 'F9'
        
        # 이미지 파일 경로 설정
        self.img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')
        self.detect_atk_path = os.path.join(self.img_dir, 'detect_atk.png')
        self.kill_mob_path = os.path.join(self.img_dir, 'kill_mob.png')
        
        self.check_image_files()

    def check_image_files(self):
        files = [self.detect_atk_path, self.kill_mob_path]
        missing_files = []
        for file in files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print("\n=== 이미지 파일 확인 필요 ===")
            print("다음 파일들이 없습니다:")
            for file in missing_files:
                print(f"- {file}")
            print("=========================\n")

    def send_key(self, key):
        win32api.keybd_event(key, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.01)

    def find_image(self, image_path):
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                grayscale=True
            )
            return location is not None
        except Exception as e:
            if not isinstance(e, pyautogui.ImageNotFoundException):
                print(f"이미지 검색 중 오류: {str(e)}")
            return False

    def try_once(self):
        try:
            # 첫 번째 시도: 6 > 방향키 > 엔터
            self.send_key(self.SKILL_KEY)  # 6
            time.sleep(0.01)
            self.send_key(self.UP_KEY)     # 방향키
            time.sleep(0.01)
            self.send_key(self.ENTER_KEY)  # 엔터
            time.sleep(0.1)  # 스킬 사용 대기

            # 스킬 사용 감지
            if self.find_image(self.detect_atk_path):
                print("공격 성공 - 킬 시도")
                
                # 6 > 엔터 반복
                kill_attempts = 0
                while kill_attempts < self.MAX_KILL_ATTEMPTS and self.is_running:
                    # 힐/마나 체크
                    if (self.macro_controller.heal_controller.is_healing or 
                        self.macro_controller.heal_controller.mana_controller.is_recovering):
                        print("힐/마나 회복을 위해 킬 시도 중단")
                        return True  # 공격은 성공했으므로 True 반환

                    self.send_key(self.SKILL_KEY)  # 6
                    time.sleep(0.01)
                    self.send_key(self.ENTER_KEY)  # 엔터
                    time.sleep(0.1)  # 킬 대기

                    if self.find_image(self.kill_mob_path):
                        print("몹 처치 성공")
                        break
                    else:
                        print("킬 시도 중...")
                        kill_attempts += 1
                        time.sleep(0.1)

                if kill_attempts >= self.MAX_KILL_ATTEMPTS:
                    print("몹 처치 실패")
                
                return True  # 공격 성공했으므로 성공 반환
            else:
                print("스킬 사용 실패")
                return False  # 공격 실패 시 다시 6>방향키>엔터 시도

        except Exception as e:
            print(f"킬러 매크로 오류: {str(e)}")
            return False
        