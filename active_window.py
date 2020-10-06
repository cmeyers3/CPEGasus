import os
import win32gui
import pyautogui

# pip3 install pywin32
# Must be Python 3.6
def get_current_window():
    if os.name == 'posix':
        pass
    elif os.name == 'nt':
        # Get current window + name
        window = win32gui.GetForegroundWindow()
        name = win32gui.GetWindowText(window)
        print("Fetching window with name: {}".format(name))

        # Get handle referring to window
        winlist = []
        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)
        hwnd = [hwnd for hwnd, title in winlist if title == name][0]

        # Make some weird adjustments to coordinates and get bounding box
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

        # Return screenshot
        return pyautogui.screenshot(region=(x, y, x1, y1))

img = get_current_window()
img.save("test_screenshot1234.jpg", "JPEG")



