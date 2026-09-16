from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

router = APIRouter(prefix="/voice", tags=["Voice Support"])
client = genai.Client()

class VoiceTranscriptionResponse(BaseModel):
    transcript_original: str
    transcript_en: str
    detected_language: str

@router.post("/transcribe", response_model=VoiceTranscriptionResponse)
async def transcribe_artisan_voice(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    mime_type = file.content_type or "audio/wav"

    prompt = (
        "You are an AI assistant for Indian rural artisans. "
        "1. Transcribe this audio recording accurately in the native language spoken (e.g. Hindi, Tamil, Telugu, etc.). "
        "2. Provide a clear English translation. "
        "3. Identify the spoken language name."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VoiceTranscriptionResponse,
                temperature=0.1,
            ),
        )
        return response.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice transcription failed: {str(e)}")