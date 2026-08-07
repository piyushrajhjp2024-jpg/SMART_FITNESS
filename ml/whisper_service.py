import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = None


def get_client():
    global client

    if client is None:
        api_key = (os.getenv("GROQ_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        client = Groq(api_key=api_key)

    return client

def speech_to_text(audio_path, language):
    """
    Convert speech audio to text using Groq Whisper.
    """

    with open(audio_path, "rb") as audio_file:

        transcription = get_client().audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="text",
            language=language   # ✅ Use the parameter
        )

    return transcription
