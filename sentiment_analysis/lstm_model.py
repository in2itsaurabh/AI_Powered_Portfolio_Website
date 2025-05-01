# sentiment_analysis/lstm_model.py
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(os.path.join(BASE_DIR, "lstm_sentiment_model.h5"))

with open(os.path.join(BASE_DIR, "tokenizer.pkl"), "rb") as f:
    tokenizer = pickle.load(f)

with open(os.path.join(BASE_DIR, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

maxlen = 200

def preprocess_and_predict(text):
    def clean_text(text):
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        return text.lower().strip()

    cleaned = clean_text(text)
    sequence = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(sequence, maxlen=maxlen, padding='post')

    pred = model.predict(padded)
    pred_index = np.argmax(pred)
    pred_label = label_encoder.inverse_transform([pred_index])[0]
    confidence_score = float(pred[0][pred_index]) * 100

    return pred_label, confidence_score
