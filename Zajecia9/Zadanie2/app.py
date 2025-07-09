import gradio as gr
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

emails = [
    "Win a free iPhone now! Click here to claim your prize!",  # Spam
    "Meeting at 10 AM tomorrow, please confirm your attendance.",  # Not Spam
    "Exclusive offer: 50% off all products this weekend only!",  # Spam
    "Project update: Please review the attached document.",  # Not Spam
    "Congratulations! You've won $1000! Call now!",  # Spam
    "Lunch plans? Let me know what you think.",  # Not Spam
]
labels = ["Spam", "Not Spam", "Spam", "Not Spam", "Spam", "Not Spam"]

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

processed_emails = [preprocess_text(email) for email in emails]

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(processed_emails)
y = np.array(labels)

classifier = MultinomialNB()
classifier.fit(X, y)

def classify_email(email_text):
    if not email_text.strip():
        return "Proszę, wpisz wiadomość e-mail."

    processed_text = preprocess_text(email_text)
    X_input = vectorizer.transform([processed_text])
    # Predict
    prediction = classifier.predict(X_input)[0]
    prob = classifier.predict_proba(X_input)[0]
    confidence = max(prob) * 100
    return f"Prediction: {prediction}\nConfidence: {confidence:.2f}%"

iface = gr.Interface(
    fn=classify_email,
    inputs=gr.Textbox(lines=5, placeholder="Wpisz treść wiadomości e-mail...", label="Treść wiadomości e-mail"),
    outputs=gr.Textbox(label="Wynik klasyfikacji"),
    title="Klasyfikator spamu w wiadomościach e-mail",
    description="Wpisz wiadomość e-mail, aby sklasyfikować ją jako Spam lub Nie Spam."
)

if __name__ == "__main__":
    iface.launch()