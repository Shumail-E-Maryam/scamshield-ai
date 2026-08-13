import re
import pandas as pd


def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " URL ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " EMAIL ", text)

    # Remove numbers
    text = re.sub(r"\d+", " NUMBER ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_dataset(path):
    df = pd.read_csv(path)

    df["message"] = df["message"].fillna("")
    df["clean_message"] = df["message"].apply(clean_text)

    return df