import pyautogui
import os

os.environ['DISPLAY'] = ':0'

im1 = pyautogui.screenshot()
im1.save(r"C:\Users\Charles\Desktop\screenshot.png")
