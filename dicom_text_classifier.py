import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib


data = r'C:\Users\olakr\OneDrive\Pulpit\WK_projekt\private_data_detection_on_DICOM_images\dataset\dicom_data3.tsv'
df = pd.read_csv(data, delimiter='\t', header=0)

print(f'Shape of data: {df.shape}')

combined_texts = df["tags"] + " " + df["value"]
labels = df["label"]

X_train, X_test, y_train, y_test = train_test_split(combined_texts, labels, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

y_pred = classifier.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

model_path = "classifier_model.pkl"
vectorizer_path = "tfidf_vectorizer.pkl"

joblib.dump(classifier, model_path)
print(f"Model zapisany w: {model_path}")

joblib.dump(vectorizer, vectorizer_path)
print(f"Wektorizer zapisany w: {vectorizer_path}")



