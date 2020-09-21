import pyautogui
import os
import sys

#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gdk

os.environ['DISPLAY'] = ':0'

im1 = pyautogui.screenshot()
im1.save('/Users/ashley/CPEGasus/tempSS/screenshot.png')

