import os

API_KEY = os.getenv("API_KEY", "dev_test_key")
ALLOWED_LANGUAGES = {
    "Tamil",
    "English",
    "Hindi",
    "Malayalam",
    "Telugu"
}

SUPPORTED_AUDIO_FORMAT = "mp3"
