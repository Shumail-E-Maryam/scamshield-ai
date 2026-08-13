import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from preprocessing import load_dataset


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = load_dataset("dataset/scam_messages.csv")

X = df["clean_message"]
y = df["label"]


# ==========================================
# 2. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 3. TF-IDF
# ==========================================

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ==========================================
# 4. TRAIN MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train_tfidf, y_train)


# ==========================================
# 5. PREDICTIONS
# ==========================================

predictions = model.predict(X_test_tfidf)


# ==========================================
# 6. EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# ==========================================
# 7. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    predictions,
    labels=["safe", "scam"]
)

print("\nConfusion Matrix:")
print(cm)


# Display confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Safe", "Scam"]
)

display.plot()

plt.title("ScamShield AI - ML Confusion Matrix")
plt.tight_layout()

plt.savefig("models/confusion_matrix.png")

plt.show()


# ==========================================
# 8. SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/scam_ml_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)


print("\nML model saved successfully!")
print("Confusion matrix saved successfully!")