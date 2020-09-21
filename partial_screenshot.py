import pyautogui
import os
import sys

#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gdk

os.environ['DISPLAY'] = ':0'
left = 100
top = 200
width = 2500
height = 1000
im1 = pyautogui.screenshot(region=(left, top, width, height))
im1.save('/Users/ashley/CPEGasus/tempSS/screenshot.png')

