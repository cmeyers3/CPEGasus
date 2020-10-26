# CPEGasus

# Group Members
- Zephan Enciso
- Charles Meyers
- Ashley Panousis
- Emory Smith

# Installation
sudo apt-get install tesseract-ocr \
pip3 install -r requirements.txt

# Bugs/ToDo
 - Handle numbers and these chars: ,.!?;:-;"/ on arduino side
 - Remove extra newline that occurs when text has an entry with more than 8 characters that contains punctuation to split it on
 - Make sure no duplicate -'s
 - Last digit of numbers being cut off. Likely not saving the carry when enter number function
 - Periods disappearing between preprocessed and processed text
 - Remove some of that random junk at the beginning of each screenshot.
