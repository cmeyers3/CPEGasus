#!/bin/python

# test_filter.py
# - Runs tesseract on given image files and returns text to stdout

import sys
import os
import re
import subprocess

import serial
import pyautogui
import pytesseract
import serial.tools.list_ports
import unidecode
from pynput import keyboard

linux_port_dir = "/dev/"
baud_rate = 57600
current = set()
hotkeys = []
if 'linux' in sys.platform:
    hotkeys = [
        {keyboard.Key.ctrl, keyboard.KeyCode(char='`')}
    ]
elif 'win32' in sys.platform:
    hotkeys = [
        {keyboard.Key.ctrl_l, keyboard.Key.tab}
    ]

def usage():
    print("Usage: python3 {}".format(sys.argv[0]))
    raise SystemExit


def get_port_name():
    '''
    Retrieves port name of Arduino for Linux or Windows OS
    '''
    # If Linux: /dev/ttyUSB* or /dev/ttyACM*
    if sys.platform == 'posix' or 'linux' in sys.platform:
        serial_ports = os.listdir(linux_port_dir)
        print("Ports: {}".format(serial_ports))
        for port in serial_ports:
            if re.match("(ttyUSB[0-9]+|ttyACM[0-9]+)", port):
                return linux_port_dir + port
            
    # If Windows: COM*
    elif sys.platform == 'win32':
        serial_ports = [p.device for p in serial.tools.list_ports.comports()]
        if len(serial_ports) > 1:
            raise SystemExit("Found multiple serial ports: {}. Exiting.".format(serial_ports))
        elif len(serial_ports) < 1:
            raise SystemExit("Found no valid serial ports. Exiting.")
        return serial_ports[0]

    # If fall through, no port found. Exit with error.
    raise SystemExit("Could not find port. Exiting.")


def get_current_window():
    # For Linux
    if sys.platform == 'posix' or 'linux' in sys.platform:

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
    
    # For Windows
    elif sys.platform == 'win32':
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
        if len(winlist) == 0:
            raise SystemExit("Error - Could not find any active windows!")
        hwnd = [hwnd for hwnd, title in winlist if title == name][0]

        # Get rid of decorations on bounding box (I think?)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

        # Return screenshot
        return pyautogui.screenshot(region=(x, y, x1, y1))
    
    # For other OS's, screenshot whole screen
    else:
        return pyautogui.screenshot()

def on_press(key):
    '''
    Runs when key is pressed to see if it is a hotkey
    '''
    if any([key in hotkey for hotkey in hotkeys]):
        print("Adding key")
        current.add(key)
        if any(all(k in current for k in hotkey) for hotkey in hotkeys):
            screenshot()

def on_release(key):
    '''
    Keeps track of keys currently pressed by deleting on release
    '''
    if any([key in hotkey for hotkey in hotkeys]):
        current.remove(key)

def screenshot():
    print("Taking Screenshot")
    # set variable to true
    os.environ['DISPLAY'] = ':0'
    
    # Decide what to screenshot and remove tab-bar  
    im = get_current_window()
    width, height = im.size
    im1 = im.crop((0, height/12, width, height))

    # Read in image, and send to pytesseract -> text
    text = pytesseract.image_to_string(im1)
    print("--------------------")
    print("Preprocessed string:")      
    print("--------------------")
    print(text)

    # Process string
    print("-----------------")
    print("Processed string:")
    print("-----------------")
    proc_text = process_text(text)
    print(proc_text)

    # Group string
    print("----------------")
    print("Grouped strings:")
    print("----------------")
    print(group_text(proc_text))


def process_text(text):
    '''
    Filters text to be ready for Braille translation
    '''
    # Allow only alphanumeric and characters in 'allowed' list
    allowed = [' ', '!', '"', '#', '-', '\'', '(', ')', ',', '-', '.', ':', ';', '?']
    text = ''.join(
        c.lower() if c.isalnum() or c in allowed else ' '
        for c in text
    )
    
    # Make substitutions
    subs = {
        '\S+\.\S+(\.\S+)?' : '',    # Get rid of websites
        '&'                : 'and', # & -> and
        '\s\s+'            : ' ',   # Multiple whitespace -> space
        '\s*:\s*'          : ':',   # Remove spaces around colons
    }
    for key, value in subs.items():
        text = re.sub(key, value, text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def pad_numbers(text):
    '''
    Pad text by adding an indicator character (#) before any numbers
    '''
    newWord = ''
    prevChar = ''

    # check if there is a number in the word
    for char in text:
        # change the group to add the padding char (#)
        if char.isdigit() and not (prevChar.isdigit() or prevChar == '#' or prevChar == '.' or prevChar == ','): 
            #if number and not already padded or formatted in a way where padding not necessary
            newWord += '#'
            newWord += char
        else:
            newWord += char
        prevChar = char
    return newWord

def split_by_punct(text):
    '''
    Takes split text and sends the correct segments from that. Returns any carry remaining
    '''
    carry = ""
    to_send = ""
    i = 7 #index of current position in to_send. Start at 7 b/c only used in more than one send
    must_send = False #exception variable to indicate must send value

    for t in text:
        if carry !="" and (t != "" and t != " ") and len(t) > 8-len(carry):
            send_word(carry)
            to_send = t
        elif carry !="" and (t != "" and t != " ") and len(t) < 8-len(carry): #less than b/c dash
            to_send = carry + ' ' + t
            must_send = True
        elif carry != "":
            next
        else:
            to_send = t
        carry = ""
        
        if len(to_send) == 8 or must_send:
            send_word(to_send)
            must_send = False
        elif len(to_send) > 8:
            # split word with dashes
            carry = split_word_with_dashes(to_send)
        elif len(to_send) < 5:
            carry = to_send

        else:
            send_word(to_send)
        
    return carry

def split_word_with_dashes(word):
    '''
    Adds dashes in words not otherwise split-able
    '''
    i = 0 # index of current position in word. Start at 7 b/c end index of first word

    while len(word[i:]) > 5:
        #check if last digit a # and move that symbol to next word
        if len(word) > i + 6:
            if word[i+6] == '#':
                send_word(word[i:i+6] + '-')
                i = i + 6
            elif word[i+6] == '-': # Remove double dashes
                send_word(word[i:i+7])
                i = i + 7
            else:
                send_word(word[i:i+7] + '-')
                i = i + 7
        else:
            send_word(word[i:i+7] + '-')
            i = i + 7
    carry = word[i:]

    return carry

def group_text(text):
    '''
    Separate text into groups of up to 8 to pass to the Arduino
    '''
    words = text.split()
    carry = "" #leftovers from previous word
    puncts = '([-:,.!?;/])'
    for word in words:
        if carry != "":
            word = carry + " " + word
        carry = "" # reset carry
        
        w = pad_numbers(word) # add in extra char if string includes a number

        if len(w) == 8:
            send_word(w)
        elif len(w) > 8:
            if ' ' in w: 
                # too long and multiple words, split those words and send
                temp = w.split()
                carry = split_by_punct(temp)
            elif any((p in puncts) for p in w): 
                # too long and other punctuation to split on, split those words and send
                temp = re.split(puncts, w)
                carry = split_by_punct(temp)      
            else: 
                # too long, split with dashes
                carry = split_word_with_dashes(w)
        elif len(w) < 5:
            # short word, save to see if combine with next word
            carry = w
        else:
            send_word(w)
    send_word(carry) # send any remaining words stored

def send_word(word):
    global ser
    '''
    Helper function to send words to Arduino via serial port.
    '''
    while(len(word) < 8):
        word = word + ' '
    
    #check if contains accented characters and translate to ascii
    norm_word = unidecode.unidecode(word)
    print("Sending: {}|\n".format(word))
    norm_word = norm_word.encode('ASCII')
    
    ser.write(norm_word)

    ard_ready = 0
    while ard_ready == 0:
        if ser.read() == '~'.encode('ASCII'):
            print("Received ~")
            ard_ready = 1


def main():
    global ser

    # Retrieve port
    port = get_port_name()
    try:
        ser = serial.Serial(port, baud_rate)
        print("Opening port {}".format(port))
    except serial.SerialException as e:
        raise SystemExit(e)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()


