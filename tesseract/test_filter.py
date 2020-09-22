# test_filter.py
# - Runs tesseract on given image files and returns text to stdout

import pytesseract
import sys
import os
import re
import pyautogui

import serial

import serial.tools.list_ports
from serial import SerialException

linux_port_dir = "/dev/"
baud_rate = 57600

def usage():
    print("Usage: py -3 {} <image file>".format(sys.argv[0]))
    raise SystemExit

def get_port_name():
    # If Linux: /dev/ttyUSB* or /dev/ttyACM*
    if os.name == 'posix':
        serial_ports = os.listdir(linux_port_dir)
        print("Ports: {}".format(serial_ports))
        for port in serial_ports:
            if re.match("(ttyUSB[0-9]+|ttyACM[0-9]+)", port):
                return port
            
    # If Windows: COM*
    elif os.name == 'nt':
        serial_ports = [p.device for p in serial.tools.list_ports.comports()]
        if len(serial_ports) > 1:
            raise SystemExit("Found multiple serial ports: {}. Exiting.".format(serial_ports))
        elif len(serial_ports) < 1:
            raise SystemExit("Found no valid serial ports. Exiting.")
        return serial_ports[0]

    # If fall through, no port found. Exit with error.
    raise SystemExit("Could not find port. Exiting.")


def parse_args():
    if len(sys.argv) <= 1:
        usage()
    args = {
        'images' : sys.argv[1:]
    }
    for image in args['images']:
        if not os.path.isfile(image):
            print("Invalid image file passed.")
            usage()

    return args

def process_text(text):
    # Allow only alphanumeric and characters in 'allowed' list
    allowed = [' ', ',', '.', '!', '-', '?', '\'', '#']
    text = ''.join(
        c.lower() if c.isalnum() or c in allowed else ' '
        for c in text
    )
    
    # Make substitutions
    subs = {
        '\S+\.\S+(\.\S+)?' : '',    # Get rid of websites
        '&'                : 'and', # & -> and
        '\.+'              : ' ',   # Ellipses -> space
        '\s\s+'            : ' ',   # Multiple whitespace -> space
    }
    for key, value in subs.items():
        text = re.sub(key, value, text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def group_text(text):
    #Separate text into groups of up to 8 to pass to the Arduino
    words = text.split()
    carry = "" #leftovers from previous word
    for w in words:
        if carry != "":
            w = carry + " " + w
        carry = "" # reset carry
        if len(w) == 8:
            send_word(w)
        elif len(w) > 8:
            if ' ' in w: 
                # too long and multiple words, split those words
                temp = w.split()
                for t in temp: 
                    # still too long, split with dashes
                    if len(t) > 8 and len(t[6:]) >5:
                        send_word(t[0:6] + '-')
                        send_word(t[6:])
                    elif len(t) > 8:
                        send_word(t[0:6] +'-')
                        carry = t[6:]
                    else:
                        send_word(t)
            else: 
                # too long, split with dashes
                send_word(w[0:6] + '-') #first 7 char and dash
                if len(w[6:]) > 5:
                    send_word(w[6:])
                else:
                    carry = w[6:]
        elif len(w) < 5:
            # short word, save to see if combine with next word
            carry = w
        else:
            send_word(w)
    send_word(carry) # send any remaining words stored

def send_word(word):
    while(len(word) < 8):
        word = word + ' '
    ser.write(string)

    ard_ready = 0
    while ard_ready == 0:
        if ser.readline() == '~':
            ard_ready = 1

def main():
    # Port
    port = get_port_name()
    try:
        ser = serial.Serial(port, baud_rate)
        print("Opening port {}".format(port))
    except SerialException:
        print("Port {} already open".format(port))
        raise SystemExit

    #screenshot
    os.environ['DISPLAY'] = ':0'
    im1 = pyautogui.screenshot()

    #for image in args['images']:
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
    print("-----------------")
    print("Grouped strings:")
    print("-----------------")
    print(group_text(proc_text))

if __name__ == '__main__':
    main()


