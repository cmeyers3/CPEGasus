import cv2
import pytesseract
import sys
import os

if not os.path.isfile(sys.argv[1]):
    print("Invalid image file passed.")
    print("Usage: py -3 {} <image file>".format(sys.argv[0]))
    raise SystemExit

img = cv2.imread(sys.argv[1])

string = pytesseract.image_to_string(img)

print("Preprocessed string:")
print(string)

print("Processed string:")
# Use regexes for this in the future
# Find websites?
string.replace('&', 'and')
string.replace('\n', ' ')
string = ''.join(c for c in string if c.isalnum() or c.isspace() or c == '\'' or c == '.' or c == '@')
print(string)


