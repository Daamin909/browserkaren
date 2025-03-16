import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

clientSTT = Groq(api_key=f'{os.getenv("API_KEY_STT")}')   
def audio_to_text(filename="temp_audio.webm"):
    AUDIO_FILE = filename
    try:
        with open(AUDIO_FILE, "rb") as file:
            transcription = clientSTT.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )
        return transcription.text
    except Exception as e:
        print(e)
        return False
    