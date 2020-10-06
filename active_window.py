import os
import re
import subprocess

import pyautogui
# sudo apt-get install scrot
# sudo apt-get install xdotool

# pip3 install pywin32
# Must be Python 3.6
def get_current_window():
    if os.name == 'posix':

        output = subprocess.check_output(
            "xwininfo -id $(xdotool getactivewindow)", shell=True
        ).decode("UTF-8")

        x1, y1, w, h = 0, 0, 0, 0
        for line in output.splitlines():
            if re.match(".*Absolute upper-left X:.*", line):
                x1 = int(line.split()[3])
            elif re.match(".*Absolute upper-left Y:.*", line):
                y1 = int(line.split()[3])
            elif re.match(".*Width:.*", line):
                w = int(line.split()[1])
            elif re.match(".*Height:.*", line):
                h = int(line.split()[1])

        return pyautogui.screenshot(region=(x1, y1, w, h))

    elif os.name == 'nt':
        import win32gui
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

        # Get rid of decorations on bounding box (I think?)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

        # Return screenshot
        return pyautogui.screenshot(region=(x, y, x1, y1))

img = get_current_window()
img.save("test_screenshot1234.jpg", "JPEG")



