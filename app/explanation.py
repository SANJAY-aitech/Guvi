import numpy as np

def generate_explanation(features: dict, prediction: str) -> str:
    pitch = features["pitch"]
    energy = features["energy"]
    zcr = features["zcr"]
    mfcc_std = np.array(features["mfcc_std"])

    reasons = []

    # ---------- AI indicators ----------
    if pitch < 110 or pitch > 260:
        reasons.append("pitch range deviates from typical human speech")

    if energy < 0.01:
        reasons.append("speech energy is unusually flat")

    if zcr < 0.05:
        reasons.append("articulation patterns appear overly consistent")

    if np.mean(mfcc_std) < 5:
        reasons.append("spectral features show limited variation")

    # ---------- Decision-aware explanation ----------
    if prediction == "AI_GENERATED":
        if reasons:
            return "; ".join(reasons)
        return "although largely human-like, subtle statistical patterns indicate synthetic speech generation"

    # ---------- HUMAN explanations (POSITIVE reasoning) ----------
    human_reasons = []

    if 120 <= pitch <= 240:
        human_reasons.append("natural pitch variation observed")

    if energy >= 0.01:
        human_reasons.append("dynamic energy patterns typical of human speech")

    if zcr >= 0.05:
        human_reasons.append("articulation patterns align with natural speech")

    if np.mean(mfcc_std) >= 5:
        human_reasons.append("rich spectral variability detected")

    # Select 1–2 strongest signals (deterministic, not random)
    return "; ".join(human_reasons[:2]) or "speech characteristics align with natural human vocal patterns"
