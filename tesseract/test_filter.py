# test_filter.py
# - Runs tesseract on given image files and returns text to stdout

import cv2
import pytesseract
import sys
import os
import re


def usage():
    print("Usage: py -3 {} <image file>".format(sys.argv[0]))
    raise SystemExit


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
    print(word)

def main():
    args = parse_args()
    for image in args['images']:
        # Read in image, and send to pytesseract -> text
        text = pytesseract.image_to_string(cv2.imread(image))
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


