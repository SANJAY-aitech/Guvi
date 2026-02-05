
# from fastapi import APIRouter, Depends, HTTPException
# from .schemas import VoiceDetectionRequest
# from .security import validate_api_key
# from .audio_processing import decode_and_extract
# from .mock_model import predict_voice
# from .utils import error_response
# from .config import ALLOWED_LANGUAGES, SUPPORTED_AUDIO_FORMAT

# router = APIRouter()

# @router.post("/api/voice-detection")
# async def voice_detection(
#     request: VoiceDetectionRequest,
#     api_key: str = Depends(validate_api_key)
# ):
#     if request.language not in ALLOWED_LANGUAGES:
#         raise HTTPException(status_code=400, detail="Unsupported language")

#     if request.audioFormat.lower() != SUPPORTED_AUDIO_FORMAT:
#         raise HTTPException(status_code=400, detail="Unsupported audio format")

#     features = decode_and_extract(request.audioBase64)
#     result = await mock_inference(features)

#     return {
#         "status": "success",
#         "language": request.language,
#         **result
#     }
from fastapi import APIRouter, Depends
from app.schemas import VoiceDetectionRequest
from app.security import validate_api_key
from app.audio_processing import decode_and_extract
from app.model import predict_voice
from app.config import ALLOWED_LANGUAGES, SUPPORTED_AUDIO_FORMAT
from app.utils import error_response

router = APIRouter()

@router.post("/api/voice-detection")
async def voice_detection(
    request: VoiceDetectionRequest,
    api_key=Depends(validate_api_key)
):
    # API key error already returned
    if api_key is not None:
        return api_key

    # Language validation
    if request.language not in ALLOWED_LANGUAGES:
        return error_response("Unsupported language")

    # Format validation
    if request.audioFormat.lower() != SUPPORTED_AUDIO_FORMAT:
        return error_response("Unsupported audio format")

    # Audio decoding
    try:
        features = decode_and_extract(request.audioBase64)
    except ValueError as e:
        return error_response(str(e))

    # ML prediction
    try:
        result = predict_voice(features)
    except RuntimeError:
        return error_response("Voice analysis failed", status_code=500)

    return {
        "status": "success",
        "language": request.language,
        **result
    }
