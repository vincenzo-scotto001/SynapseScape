import pyautogui
import ctypes

class OSRSGame:
    def __init__(self):
        # Find the game window
        self.game_window = None
        user32 = ctypes.windll.user32
        user32.EnumWindows(self.enum_windows_callback, 0)

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
            if title.value == 'Runelite':
                self.game_window = hwnd
        return True

    def get_window_rect(self):
        # Get the game window position and size
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(self.game_window, ctypes.byref(rect))
        return rect.left, rect.top, rect.right, rect.bottom
