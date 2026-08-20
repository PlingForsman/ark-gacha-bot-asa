import win32gui

def find_window_by_title(junk: str) -> int | None:
    result = []

    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        
        title = win32gui.GetWindowText(hwnd)
        if not title.lower().startswith("ark: survival ascended"):
            return
        
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        if (right - left, bottom - top) in {(1920, 1080), (2560, 1440)}:
            result.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return result[0] if result else None

HWND = find_window_by_title("ArkAscended")