from text_detector_ocr import text_detector
from text_classifier import text_classifier
from anonimization_text import blur_sensitive_text, mask_sensitive_text
import cv2

#ścieżka do pliku dicom oraz modeli
image_path = r'test_image\f538813c-93c7-40a2-8f5a-139ae11d7a6a.jpg'
model_path = "model/classifier_model.pkl"
vectorizer_path = "model/tfidf_vectorizer.pkl"

#wyodrębnienie oraz wykrycie tekstu na zdjęciach
merged_words, merged_words_with_coordinates, image = text_detector(image_path)

#klasyfikacja
words_with_sensitivity = text_classifier(merged_words, model_path, vectorizer_path)

colors = {
    0: (0, 255, 0),  
    1: (0, 0, 255), 
}

#oznakowanie zdjęcia
for group in merged_words_with_coordinates:
    word = group['text']
    coordinates = group['coordinates']
    
    sensitivity = next((s[1] for s in words_with_sensitivity if s[0] == word), None)
    
    if sensitivity is not None:
        top_left = coordinates[0] 
        bottom_right = coordinates[2]  

        color = colors.get(sensitivity, (255, 255, 255))  

        cv2.rectangle(image, top_left, bottom_right, color, 2)


start_x = int(image.shape[1] / 2) - 100
start_y = 20

# cv2.putText(image, f"Zielony: Dane niewrazliwe", (start_x, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)    
# cv2.putText(image, f"Czerwony: Dane wrazliwe", (start_x, start_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)    
# Przykład wywołania z czarnym prostokątem

image_mask = image.copy()  # Tworzymy kopię obrazu do operacji maskowania
image_mask = mask_sensitive_text(image_mask, merged_words_with_coordinates, words_with_sensitivity, colors)

image_blur = image.copy()  # Tworzymy kopię obrazu do operacji rozmycia
image_blur = blur_sensitive_text(image_blur, merged_words_with_coordinates, words_with_sensitivity, colors)

cv2.imshow('Image with detected and classified text', image)
cv2.imshow('Image with blur overlay', image_blur)
cv2.imshow('Image with mask overlay', image_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.destroyAllWindows()