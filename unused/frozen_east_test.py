import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import matplotlib.pyplot as plt
from PIL import Image
import easyocr

img = cv2.imread(r'ouput2\7_r8_1-53_173723367526222.png')

model = cv2.dnn.readNet('frozen_east_text_detection.pb')

height, width, _ = img.shape
new_height = (height // 32) * 32
new_width = (width // 32) * 32
print(new_height, new_width)

h_ratio = height / new_height
w_ratio = width / new_width
print(h_ratio, w_ratio)

blob = cv2.dnn.blobFromImage(img, 1, (new_width, new_height), (123.68, 116.78, 103.94), True, False)
model.setInput(blob)

(geometry, scores) = model.forward(model.getUnconnectedOutLayersNames())

rectangles = []
confidence_score = []
for i in range(geometry.shape[2]):
    for j in range(geometry.shape[3]):
        if scores[0][0][i][j] < 0.1:
            continue

        bottom_x = int(j * 4 + geometry[0][1][i][j])
        bottom_y = int(i * 4 + geometry[0][2][i][j])
        top_x = int(j * 4 - geometry[0][3][i][j])
        top_y = int(i * 4 - geometry[0][0][i][j])

        rectangles.append((top_x, top_y, bottom_x, bottom_y))
        confidence_score.append(float(scores[0][0][i][j]))

final_boxes = non_max_suppression(np.array(rectangles), probs=confidence_score, overlapThresh=0.5)

reader = easyocr.Reader(['en', 'pl'])  

img_copy = img.copy()
for x1, y1, x2, y2 in final_boxes:
    y1 = max(0, y1 - 1)
    y2 = min(img.shape[0], y2 + 1)
    x1 = max(0, x1 - 1)
    x2 = min(img.shape[1], x2 + 1)

    cropped_img = img[y1:y2, x1:x2]

    result = reader.readtext(cropped_img)

    if result:
        text = result[0][1]  
        print(text)
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Detected Text', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
