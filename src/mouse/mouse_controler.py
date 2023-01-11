import pyautogui

from models.GestureEnum import Gesture


class MouseController:
    def __init__(self) -> None:
        pass

    def left_click(self):
        pyautogui.leftClick()
    
    def right_click(self):
        pyautogui.rightClick()

    def zoom_in(self):
        pyautogui.keyDown('ctrlleft')
        self.scroll_up()
        pyautogui.keyUp('ctrlleft')

    def zoom_out(self):
        pyautogui.keyDown('ctrlleft')
        self.scroll_down()
        pyautogui.keyUp('ctrlleft')

    def tab_window(self):
        pyautogui.keyDown('altleft')
        pyautogui.press('tab')
        pyautogui.keyUp('altleft')

    def scroll_up(self):
        pyautogui.scroll(100)

    def scroll_down(self):
        pyautogui.scroll(-100)

    def move_mouse(self, direction):
        """
            Direction : Tuple (float, float) Represents (x,y) direction
        """
        #print(f"Moving to {(x+direction[0], y+direction[1])}")
        pyautogui.move(direction[0], -direction[1])

    def apply_state(self, action):
        #print(f"Applying state {action}")
        if action == Gesture.NONE.value:
            pass
        elif action == Gesture.RIGHT_INDEX_EXTENDED.value:
            pass
        elif action == Gesture.RIGHT_INDEX_HOOK.value:
            pass
        elif action == Gesture.RIGHT_INDEX_CLOSED.value:
            self.right_click()
        elif action == Gesture.LEFT_INDEX_EXTENDED.value:
            pass
        elif action == Gesture.LEFT_INDEX_HOOK.value:
            pass
        elif action == Gesture.LEFT_INDEX_CLOSED.value:
            self.left_click()
        elif action == Gesture.PINCH_IN.value:
            self.zoom_in()
        elif action == Gesture.PINCH_OUT.value:
            self.zoom_out()
        elif action == Gesture.THUMB_UP.value:
            self.scroll_up()
        elif action == Gesture.THUMB_DOWN.value:
            self.scroll_down()
        elif action == Gesture.EXTENDED_HAND_START.value:
            pass
        elif action == Gesture.EXTENDED_HAND_END.value:
            self.tab_window()

