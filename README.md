# AI vs Human Voice Detection API

A FastAPI-based service that classifies short voice samples as AI-generated or Human-generated using acoustic features and a trained ML model.

Key points:
- Language support: Tamil, English, Hindi, Malayalam, Telugu
- Accepts Base64-encoded MP3 audio
- Returns classification, confidence score, and a feature-based explanation
- API-key protected endpoint for production safety

## Repository structure

- [app](app) — FastAPI application code (routes, processing, model wrapper)
- [ai_voices.py](ai_voices.py) — auxiliary script
- [voice_model.joblib](voice_model.joblib) — trained classifier (must exist at repo root)
- [feature_scaler.joblib](feature_scaler.joblib) — feature scaler used at inference
- [sentences.txt](sentences.txt) — example data
- [ML](ML) — training scripts and data
- [requirements.txt](requirements.txt) — Python deps
- [Procfile](Procfile) — command used for deploy (Heroku-like)

## Requirements

- Python 3.8+
- See [requirements.txt](requirements.txt) for exact packages. Example important packages: `fastapi`, `uvicorn`, `numpy`, `scikit-learn`, `librosa`, `soundfile`, `joblib`.

## Setup (local development)

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Or (CMD):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Ensure the model artifacts exist at the repository root:

- [voice_model.joblib](voice_model.joblib)
- [feature_scaler.joblib](feature_scaler.joblib)

If you don't have them, check [ML/train.py](ML/train.py) to retrain or ask the maintainer for the artifacts.

## Environment variables

- `API_KEY` — API key used by the service. Defaults to `dev_test_key` when not set (see [app/config.py](app/config.py)).
- `PORT` — port used by the server (production envs such as Heroku set this automatically).

## Running

- Development (reload on change):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Production / Procfile (Heroku style):

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set a custom API key before starting if desired (PowerShell):

```powershell
$env:API_KEY = "your_key_here"
uvicorn app.main:app --reload --port 8000
```

## API

Base URL (local): `http://127.0.0.1:8000`

- Health check

	- GET `/health`
	- Response: `{ "status": "OK" }`

- Voice detection

	- POST `/api/voice-detection`
	- Protected: requires header `X-API-KEY` with the value of `API_KEY`.
	- Request JSON schema (`VoiceDetectionRequest`):

		```json
		{
			"language": "Tamil",
			"audioFormat": "mp3",
			"audioBase64": "<base64-encoded-mp3>"
		}
		```

	- Success response (`VoiceDetectionResponse`):

		```json
		{
			"status": "success",
			"language": "Tamil",
			"classification": "AI_GENERATED",
			"confidenceScore": 0.95,
			"explanation": "...feature-based explanation..."
		}
		```

### Example curl (health)

```bash
curl http://127.0.0.1:8000/health
```

### Example curl (voice detection)

```bash
curl -X POST http://127.0.0.1:8000/api/voice-detection \
	-H "Content-Type: application/json" \
	-H "X-API-KEY: dev_test_key" \
	-d '{"language":"Tamil","audioFormat":"mp3","audioBase64":"<BASE64>"}'
```

### Example Python request

```python
import base64
import requests

with open('sample.mp3','rb') as f:
		b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
		'language': 'Tamil',
		'audioFormat': 'mp3',
		'audioBase64': b64
}

res = requests.post('http://127.0.0.1:8000/api/voice-detection', json=payload, headers={'X-API-KEY':'dev_test_key'})
print(res.json())
```

## Troubleshooting

- Invalid API key → set `API_KEY` env var or use `dev_test_key` during local dev.
- Unsupported language → use one of: Tamil, English, Hindi, Malayalam, Telugu.
- Unsupported audio format → service expects MP3 (`audioFormat: "mp3"`).
- Missing model files → ensure [voice_model.joblib](voice_model.joblib) and [feature_scaler.joblib](feature_scaler.joblib) exist at repo root.

## Notes for maintainers

- The inference logic lives in [app/model.py](app/model.py) and uses `joblib` to load the model and scaler.
- Audio decoding and feature extraction happen in [app/audio_processing.py](app/audio_processing.py).
- Request/response schemas are defined in [app/schemas.py](app/schemas.py).

---

If you'd like, I can also add a short example `sample_request.py` and a `tests/` folder with a basic health-check test. Tell me which you'd prefer next.

