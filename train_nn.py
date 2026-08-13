import joblib
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from preprocessing import load_dataset


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = load_dataset("dataset/scam_messages.csv")

X = df["clean_message"]
y = df["label"]


# Convert labels:
# safe = 0
# scam = 1

y = y.map({
    "safe": 0,
    "scam": 1
})


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
# 3. LOAD TF-IDF VECTORIZER
# ==========================================

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# Transform text into numerical vectors

X_train_tfidf = vectorizer.transform(X_train).toarray()
X_test_tfidf = vectorizer.transform(X_test).toarray()


print("TF-IDF features:", X_train_tfidf.shape[1])


# ==========================================
# 4. BUILD NEURAL NETWORK
# ==========================================

model = tf.keras.Sequential([

    tf.keras.layers.Input(
        shape=(X_train_tfidf.shape[1],)
    ),

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(
        1,
        activation="sigmoid"
    )
])


# ==========================================
# 5. COMPILE MODEL
# ==========================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# ==========================================
# 6. SHOW ARCHITECTURE
# ==========================================

model.summary()


# ==========================================
# 7. TRAIN
# ==========================================

history = model.fit(
    X_train_tfidf,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)


# ==========================================
# 8. PREDICTIONS
# ==========================================

probabilities = model.predict(
    X_test_tfidf
)

predictions = (
    probabilities >= 0.5
).astype(int).flatten()


# ==========================================
# 9. EVALUATION
# ==========================================

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nNeural Network Accuracy:", accuracy)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=["safe", "scam"]
    )
)


# ==========================================
# 10. SAVE MODEL
# ==========================================

model.save(
    "models/scam_neural_network.keras"
)

print("\nNeural Network saved successfully!")