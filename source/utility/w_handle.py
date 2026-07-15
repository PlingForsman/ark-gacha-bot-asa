from ctypes import wintypes
import ctypes

def find_window_by_title(junk: str) -> int:
    result = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def enum_handler(hwnd, _):
        if not ctypes.windll.user32.IsWindowVisible(hwnd):
            return True

        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
        title: str = buffer.value

        if not title.lower().startswith("ark: survival ascended"):
            return True

        rect = wintypes.RECT()
        ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
        if (rect.right - rect.left, rect.bottom - rect.top) in {(1920, 1080), (2560, 1440)}:
            result.append(hwnd)

        return True

    ctypes.windll.user32.EnumWindows(enum_handler, 0)
    return result[0] if result else None

HWND = find_window_by_title("ArkAscended")