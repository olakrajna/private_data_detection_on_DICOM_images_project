import easyocr
import cv2

image_path = r'ouput\99_r5_1-299_173402856859067.png'
image = cv2.imread(image_path)

reader = easyocr.Reader(['en', 'pl'])
result = reader.readtext(image_path)

for res in result:
    top_left = tuple(map(int, res[0][0]))
    bottom_right = tuple(map(int, res[0][2]))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    print(res)
   
cv2.imshow('OCR Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

