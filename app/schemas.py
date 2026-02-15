from pydantic import BaseModel, Field

class VoiceDetectionRequest(BaseModel):
    language: str = Field(..., example="Tamil")
    audioFormat: str = Field(..., example="mp3")
    audioBase64: str

class VoiceDetectionResponse(BaseModel):
    status: str
    classification: str
    confidenceScore: float

