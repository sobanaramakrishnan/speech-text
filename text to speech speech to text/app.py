from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import os
import speech_recognition as sr

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Serve the HTML frontend.
    """
    with open("index.html", "r") as f:
        return f.read()

@app.post("/tts")
async def text_to_speech(text: str = Form(...)):
    """
    Convert text to speech and return the audio file.
    """
    tts = gTTS(text=text, lang="en")
    file_path = "static/output.mp3"
    tts.save(file_path)
    return {"audio_url": f"/static/output.mp3"}

@app.post("/stt")
async def speech_to_text():
    """
    Real-time speech-to-text processing.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        return {"Transcribed Text": text}
    except sr.UnknownValueError:
        return {"Error": "Speech could not be understood."}
    except sr.RequestError as e:
        return {"Error": f"Could not request results; {e}"}
