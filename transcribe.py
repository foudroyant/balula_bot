import assemblyai as aai
import os
from dotenv import load_dotenv
load_dotenv()

ASSEMBLYAI_KEY = os.getenv("ASSEMBLYAI_KEY")
aai.settings.api_key = ASSEMBLYAI_KEY

def transcription(url_file, lng="fr"):
    print(lng)
    transcriber = aai.Transcriber(config=aai.TranscriptionConfig(
        speech_model='nano', 
        language_code=lng
    ))
    transcript = transcriber.transcribe(url_file)
    print(transcript.text)

    return transcript.text