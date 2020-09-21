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
        print(process_text(text))

if __name__ == '__main__':
    main()


