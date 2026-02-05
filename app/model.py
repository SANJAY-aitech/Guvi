import numpy as np
import joblib
from app.explanation import generate_explanation

# Load once at startup (IMPORTANT)
model = joblib.load("voice_model.joblib")
scaler = joblib.load("feature_scaler.joblib")

def predict_voice(features: dict):
    # Build feature vector in SAME order as training
    x = np.array([[
        *features["mfcc_mean"],
        *features["mfcc_std"],
        features["pitch"],
        features["energy"],
        features["zcr"]
    ]])

    # Scale
    x = scaler.transform(x)

    # Predict probability
    prob = model.predict_proba(x)[0][1]

    explanation = generate_explanation(features)

    if prob >= 0.5:
        return {
            "classification": "AI_GENERATED",
            "confidenceScore": round(float(prob), 2),
            "explanation": explanation
        }
    else:
        return {
            "classification": "HUMAN",
            "confidenceScore": round(float(1 - prob), 2),
            "explanation": explanation
        }
