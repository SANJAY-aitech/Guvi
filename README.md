# AI vs Human Voice Detection API

This project provides a secure REST API that detects whether a given voice sample is
AI-generated or Human-generated using acoustic feature analysis and a trained
machine learning model.

The system is designed according to GUVI hackathon constraints and does not use
any external AI detection APIs.

---

## 🔍 Features
- Accepts Base64-encoded MP3 audio
- Supports Tamil, English, Hindi, Malayalam, and Telugu
- ML-based classification (AI_GENERATED / HUMAN)
- Confidence score (0.0 – 1.0)
- Feature-driven explanation (non-hardcoded)
- API key–protected endpoint

---
