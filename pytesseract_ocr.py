from PIL import Image
import pytesseract
import numpy as np
import cv2
import matplotlib.pyplot as plt 
from pytesseract import Output
import cv2

import cv2

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

#BIAŁE ZDJĘCIE
filename = r'C:\Users\olakr\OneDrive\Pulpit\DICOM_generator\ouput\56_r6_1-17_173402856859015.png'

# filename = r'C:\Users\olakr\OneDrive\Pulpit\DICOM_generator\ouput\97_r8_1-32_173402856859077.png'

img = cv2.imread(filename)

# img = cv2.bitwise_not(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.GaussianBlur(img, (3, 3), .25)
# cv2.imwrite("g.jpg", img)

#DOBRE USTAWIENIA DLA BIAŁYCH ZDJĘĆ + inverted + grayscale (lub sam inverted)
# thresh, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)

#Teraz szuakm dla czarnego
# thresh, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY )

# img = cv2.adaptiveThreshold(img, 210, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 5)


d = pytesseract.image_to_data(img, output_type=Output.DICT)
text = pytesseract.image_to_string(Image.open(filename), config='--psm 8')

print(d.keys())
print(d['conf'])

print('text', text)

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)