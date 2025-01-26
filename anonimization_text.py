import cv2
import numpy as np

def blur_sensitive_text(image, merged_words_with_coordinates, words_with_sensitivity, colors):
    start_y = 10  
    for group in merged_words_with_coordinates:
        word = group['text']
        coordinates = group['coordinates']
        
        sensitivity = next((s[1] for s in words_with_sensitivity if s[0] == word), None)
        
        if sensitivity is not None:
            top_left = coordinates[0]
            bottom_right = coordinates[2]
            
            if sensitivity == 1:
                roi = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]  
                blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0) 
                image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = blurred_roi 
            else:
                color = colors.get(sensitivity, (255, 255, 255))
                cv2.rectangle(image, top_left, bottom_right, color, 2)
            
            start_y += 30  

    return image

import cv2
import numpy as np

def mask_sensitive_text(image, merged_words_with_coordinates, words_with_sensitivity, colors):
    start_y = 10  

    for group in merged_words_with_coordinates:
        word = group['text']
        coordinates = group['coordinates']
        
        sensitivity = next((s[1] for s in words_with_sensitivity if s[0] == word), None)
        
        if sensitivity is not None:
            top_left = coordinates[0]
            bottom_right = coordinates[2]
            
            if sensitivity == 1:
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)  
            else:
                color = colors.get(sensitivity, (255, 255, 255))
                cv2.rectangle(image, top_left, bottom_right, color, 2)
            
            start_y += 30 

    return image
