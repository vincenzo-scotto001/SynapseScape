import pyautogui
import ctypes
import time

from ctypes import wintypes
from utils import smooth_move_bezier

class OSRSGame:
    def __init__(self):
        # Find the game window
        self.game_window = None
        user32 = ctypes.windll.user32
        
        #user32.EnumWindows(self.enum_windows_callback, 0)
        ENUM_WINDOWS_PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(ENUM_WINDOWS_PROC(self.enum_windows_callback), 0)

        if not self.game_window:
            raise Exception("Could not find Runelite window")

        # Get the game window position and size
        self.left, self.top, self.right, self.bottom = self.get_window_rect()

    def press_key(self, key):
        # Press a keyboard key
        ctypes.windll.user32.keybd_event(ord(key), 0, 0, 0)
        ctypes.windll.user32.keybd_event(ord(key), 0, 2, 0)

    def move_mouse(self, x, y):
        # Move the mouse to a position within the game window
        pyautogui.moveTo(self.left + x, self.top + y)

    def click_mouse(self, button='left'):
        # Click the mouse button within the game window
        button = button.lower()
        if button == 'left':
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
        elif button == 'right':
            ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
        else:
            raise ValueError(f"Invalid button: {button}")

    def enum_windows_callback(self, hwnd, lParam):
        # Callback function for EnumWindows that checks for the game window
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd) + 1
            title = ctypes.create_unicode_buffer(length)
            ctypes.windll.user32.GetWindowTextW(hwnd, title, length)
            if title.value == 'RuneLite':
                self.game_window = hwnd
        return True

    def get_window_rect(self):
        # Get the game window position and size
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(self.game_window, ctypes.byref(rect))
        return rect.left, rect.top, rect.right, rect.bottom
        
    def get_cursor_position_rel(self):
        # Get the position of the mouse cursor within the game window relative to the bottom-left corner of the game window
        cursor = wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        relative_x = cursor.x - self.left
        relative_y = self.bottom - cursor.y
        return relative_x, relative_y
    
    def get_cursor_position_abs(self):
        cursor = wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        return cursor.x, cursor.y

    def show_cursor_position(self):
        while True:
            game_x, game_y = self.get_cursor_position_rel()
            print(f"Cursor position relative to game window center: ({game_x}, {game_y})")
            time.sleep(0.1)

game = OSRSGame()
size = (game.right - game.left, game.bottom - game.top)
print(size)
game.show_cursor_position()
#game.move_mouse(734, 672)
#smooth_move_bezier((-.25, 0.5), (.75, .5), duration=2, complexity=4, steps=50, window_size=size)