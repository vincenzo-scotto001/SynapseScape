# actionhandler.py
import pyautogui
import win32gui
import win32api
import win32con

class OSRSGame:
    def __init__(self):
        # Find the game window
        self.game_window = None
        windows = []
        win32gui.EnumWindows(lambda hwnd, windows: windows.append(hwnd), windows)
        for hwnd in windows:
            if win32gui.GetWindowText(hwnd) == 'Old School RuneScape':
                self.game_window = hwnd
                break

        if not self.game_window:
            raise Exception("Could not find Old School RuneScape window")

        # Get the game window position and size
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.game_window)

    def press_key(self, key):
        # Press a keyboard key
        vk_code = win32api.MapVirtualKey(ord(key), win32con.MAPVK_VK_TO_VSC)
        win32api.keybd_event(vk_code, 0, 0, 0)
        win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

    def move_mouse(self, x, y):
        # Move the mouse to a position within the game window
        pyautogui.moveTo(self.left + x, self.top + y)

    def click_mouse(self, button='left'):
        # Click the mouse button within the game window
        button = button.lower()
        if button == 'left':
            win32api.SendMessage(self.game_window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
            win32api.SendMessage(self.game_window, win32con.WM_LBUTTONUP, 0, 0)
        elif button == 'right':
            win32api.SendMessage(self.game_window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, 0)
            win32api.SendMessage(self.game_window, win32con.WM_RBUTTONUP, 0, 0)
        else:
            raise ValueError(f"Invalid button: {button}")
