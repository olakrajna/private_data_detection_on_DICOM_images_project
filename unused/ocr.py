import easyocr
import cv2
import spacy
import re

# Funkcja do wykrywania danych wrażliwych w danych tekstowych z uwzględnieniem kontekstu
def detect_sensitive_data_with_context(data):
    # Zdefiniowane wzorce dla danych wrażliwych
    regex_patterns = {
        "Time": r'\b\d{6}(\.\d+)?\b',
        "Date": r'\b\d{8}\b',
        "StudyID": r'\b\d{6}\b',
        "AccessionNumber": r'\b\d{13,16}\b',
        "PatientName": r'\b[A-Z][a-z]+\b',  # Tylko jedno słowo z dużą literą na początku
        "PatientID": r'\b[A-Z]{3}\d{6}\b',
        "PhysicianName": r'\b[A-Z][a-z]+\b',
        "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    }

    # Słowa kluczowe, które będą szukały kontekstu (np. "Patient Name", "Study Time")
    context_keywords = {
        "Time": ["Study Time", "Content Time", "Acquisition Time", "Time"],
        "Date": ["Study Date", "Content Date", "Content", "Acquisition Date", "Series Date", "Series", "Acquisition"],
        "PatientName": ["Patient Name", "Patient"],
        "PatientID": ["Patient ID", "Patient", "ID"],
        "PhysicianName": ["Referring Physicians Name"],
        "Email": ["Email"],
        "StudyID": ["Study ID"],
        "AccessionNumber": ["Accession Number"]
    }

    sensitive_data = []

    # Przeszukaj dane w poszukiwaniu kontekstu i dopasuj wzorce
    for category, patterns in context_keywords.items():
        for keyword in patterns:
            for text in data:
                if keyword.lower() in text.lower():  # Dopasowanie bez względu na wielkość liter
                    match = re.search(regex_patterns[category], text)
                    if match:
                        sensitive_data.append((category, match.group()))

    return sensitive_data


# Wczytywanie obrazu
image_path = r'ouput2\70_r2_1-55_17372336752624.png'
image = cv2.imread(image_path)

# Wczytanie modelu spacy
nlp = spacy.load("en_core_web_sm")

# Odczyt danych z obrazu
reader = easyocr.Reader(['en', 'pl'])
result = reader.readtext(image_path)
result_witout_detail = reader.readtext(image_path, detail=0)

print(result_witout_detail)

# Przeszukiwanie wykrytych danych pod kątem danych wrażliwych
# detected_data = detect_sensitive_data_with_context(result_witout_detail)
# for category, value in detected_data:
#     print('Wykryte')
#     print(f"{category}: {value}")

# Rysowanie prostokątów na obrazie
for res in result:
    top_left = tuple(map(int, res[0][0]))
    bottom_right = tuple(map(int, res[0][2]))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    print(res)

# Przeszukiwanie za pomocą spaCy
for res in result_witout_detail:
    doc = nlp(res)

    for entity in doc.ents:
        print(entity.label_ + ": " + entity.text)

# Wyświetlenie obrazu z zaznaczonymi danymi
cv2.imshow('OCR Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
