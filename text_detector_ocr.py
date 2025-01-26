
import cv2
import easyocr

def is_similar_height(coord1, coord2, threshold=10):
    y1_top, y1_bottom = coord1[0][1], coord1[2][1]
    y2_top, y2_bottom = coord2[0][1], coord2[2][1]
    return abs(y1_top - y2_top) <= threshold or abs(y1_bottom - y2_bottom) <= threshold

def is_close_in_x(coord1, coord2, threshold=100):
   
    x1_right = coord1[2][0]
    x2_left = coord2[0][0]
    return abs(x2_left - x1_right) <= threshold

def text_detector(image_path: str) -> list:
    print("Rozpoczęto proces detekcji tekstu na obrazie.. ")
    image = cv2.imread(image_path)
    reader = easyocr.Reader(['en', 'pl'])
    result = reader.readtext(image_path)
    print("Wykryto tekst..")

    merged_words_with_coordinates = []
    merged_words = []

    print("Przetwarzanie tekstu..")
    for res in result:
        top_left = tuple(map(int, res[0][0]))
        bottom_right = tuple(map(int, res[0][2]))
        word = res[1]

        merged = False
        for i, group in enumerate(merged_words_with_coordinates):
            if is_similar_height(group['coordinates'], res[0]) and is_close_in_x(group['coordinates'], res[0]):
                group['text'] += f" {word}"
                merged_words[i] +=  f" {word}"

                group['coordinates'][0] = (
                    min(group['coordinates'][0][0], top_left[0]),
                    min(group['coordinates'][0][1], top_left[1])
                )

                group['coordinates'][2] = (
                    max(group['coordinates'][2][0], bottom_right[0]),
                    max(group['coordinates'][2][1], bottom_right[1])
                )
                merged = True
                break

        if not merged:
            merged_words_with_coordinates.append({
                'text': word,
                'coordinates': [top_left, res[0][1], bottom_right, res[0][3]]
            })

            merged_words.append(
                word
            )
            
    return merged_words, merged_words_with_coordinates, image

