import re
import joblib
import numpy as np
import tensorflow as tf

from preprocessing import clean_text


# ==========================================
# LOAD MODELS
# ==========================================

ml_model = joblib.load(
    "models/scam_ml_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)

nn_model = tf.keras.models.load_model(
    "models/scam_neural_network.keras"
)

# ==========================================
# RISK INDICATORS
# ==========================================

def detect_risk_indicators(message):

    text = message.lower()

    indicators = []


    # --------------------------------------
    # Urgency
    # --------------------------------------

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "right now",
        "last warning",
        "within 24 hours",
        "expires today",
        "final notice"
    ]

    if any(word in text for word in urgency_words):
        indicators.append(
            "Urgent or threatening language detected"
        )


    # --------------------------------------
    # Financial requests
    # --------------------------------------

    financial_words = [
        "send money",
        "transfer money",
        "bank account",
        "credit card",
        "debit card",
        "payment",
        "pay",
        "fee",
        "cash",
        "refund"
    ]

    if any(word in text for word in financial_words):
        indicators.append(
            "Financial or payment-related request detected"
        )


    # --------------------------------------
    # Credentials / OTP
    # --------------------------------------

    credential_words = [
        "otp",
        "one time password",
        "password",
        "pin",
        "verification code",
        "login",
        "account details",
        "security code"
    ]

    if any(word in text for word in credential_words):
        indicators.append(
            "Sensitive credential or verification information requested"
        )


    # --------------------------------------
    # Prize / reward
    # --------------------------------------

    prize_words = [
        "winner",
        "won",
        "prize",
        "reward",
        "lottery",
        "free entry",
        "claim"
    ]

    if any(word in text for word in prize_words):
        indicators.append(
            "Prize or reward language detected"
        )


    # --------------------------------------
    # URLs
    # --------------------------------------

    url_pattern = r"(https?://\S+|www\.\S+)"

    if re.search(url_pattern, text):
        indicators.append(
            "URL or web link detected"
        )


    # --------------------------------------
    # Phone numbers
    # --------------------------------------

    phone_pattern = r"\+?\d[\d\s\-]{7,}\d"

    if re.search(phone_pattern, text):
        indicators.append(
            "Phone number detected"
        )


    return indicators


# ==========================================
# RECOMMENDATION
# ==========================================

def get_recommendation(score):

    if score >= 75:

        return (
            "HIGH RISK: Do not click links, send money, "
            "share OTPs, passwords, or banking information. "
            "Verify the sender through an official channel."
        )

    elif score >= 50:

        return (
            "MODERATE RISK: Be cautious. "
            "Verify the sender independently before "
            "clicking links or sharing information."
        )

    elif score >= 25:

        return (
            "LOW-MODERATE RISK: Some suspicious characteristics "
            "were detected. Avoid sharing sensitive information."
        )

    else:

        return (
            "LOW RISK: The message does not show strong "
            "scam characteristics, but remain cautious."
        )


# ==========================================
# MAIN ANALYZER
# ==========================================

def analyze_message(message):

    # Clean text
    cleaned = clean_text(message)


    # TF-IDF
    features = vectorizer.transform(
        [cleaned]
    )


    # --------------------------------------
    # ML probability
    # --------------------------------------

    ml_probability = ml_model.predict_proba(
        features
    )[0]


    ml_scam_index = list(
        ml_model.classes_
    ).index("scam")


    ml_score = (
        ml_probability[ml_scam_index] * 100
    )


    # --------------------------------------
    # Neural Network probability
    # --------------------------------------

    nn_features = features.toarray()

    nn_probability = nn_model.predict(
        nn_features,
        verbose=0
    )[0][0]


    nn_score = nn_probability * 100


    # --------------------------------------
    # Model combination
    # --------------------------------------

    model_score = (
        (ml_score * 0.4) +
        (nn_score * 0.6)
    )


    # --------------------------------------
    # Rule-based indicators
    # --------------------------------------

    indicators = detect_risk_indicators(
        message
    )


    # --------------------------------------
    # Indicator bonus
    # --------------------------------------

    indicator_bonus = min(
        len(indicators) * 4,
        20
    )


    # --------------------------------------
    # Final risk score
    # --------------------------------------

    final_score = min(
        model_score + indicator_bonus,
        100
    )


    # --------------------------------------
    # Risk level
    # --------------------------------------

    if final_score >= 75:

        risk_level = "HIGH RISK"

    elif final_score >= 50:

        risk_level = "MEDIUM RISK"

    elif final_score >= 25:

        risk_level = "LOW-MEDIUM RISK"

    else:

        risk_level = "LOW RISK"


    # --------------------------------------
    # Recommendation
    # --------------------------------------

    recommendation = get_recommendation(
        final_score
    )


    return {

        "risk_score": round(
            final_score,
            2
        ),

        "risk_level": risk_level,

        "ml_score": round(
            ml_score,
            2
        ),

        "nn_score": round(
            nn_score,
            2
        ),

        "indicators": indicators,

        "recommendation": recommendation

    }