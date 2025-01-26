
import joblib

def text_classifier(data: list, model_path: str, vectorizer_path: str):

    print(data)
    words_with_sensitivity = []

    loaded_classifier = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)

    new_tfidf = loaded_vectorizer.transform(data)

    new_predictions = loaded_classifier.predict(new_tfidf)

    for item, prediction in zip(data, new_predictions):
        sensitivity = "Sensitive" if prediction == 1 else "Not Sensitive"
        words_with_sensitivity.append((item, prediction) )
        print(f"{item} -> {sensitivity}")
    
    return words_with_sensitivity