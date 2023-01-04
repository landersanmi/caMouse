import pyautogui
from pyautogui import K
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
        pyautogui.scroll(10)

    def scroll_down(self):
        pyautogui.scroll(-10)

    def move_mouse(self, direction):
        """
            Direction : Tuple (float, float) Represents (x,y) direction
        """
        x, y = pyautogui.position()
        pyautogui.move(x+direction[0], y+direction[1])

    def apply_state(self, action):
        #TODO Remove unused checks if movable state is removed
        if action == Gesture.NONE:
            pass
        elif action == Gesture.RIGHT_INDEX_EXTENDED:
            pass
        elif action == Gesture.RIGHT_INDEX_HOOK:
            pass
        elif action == Gesture.RIGHT_INDEX_CLOSED:
            self.right_click()
        elif action == Gesture.LEFT_INDEX_EXTENDED:
            pass
        elif action == Gesture.LEFT_INDEX_HOOK:
            pass
        elif action == Gesture.LEFT_INDEX_CLOSED:
            self.left_click()
        elif action == Gesture.PINCH_IN:
            self.zoom_in()
        elif action == Gesture.PINCH_OUT:
            self.zoom_out()
        elif action == Gesture.THUMB_UP:
            self.scroll_up()
        elif action == Gesture.THUMB_DOWN:
            self.scroll_down()
        elif action == Gesture.EXTENDED_HAND_START:
            pass
        elif action == Gesture.EXTENDED_HAND_END:
            self.tab_window()

