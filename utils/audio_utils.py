import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import tempfile
import os
import streamlit as st

def text_to_speech_autoplay(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None


def transcribe_audio(audio_bytes):
    r = sr.Recognizer()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_filename = temp_audio.name

    try:
        with sr.AudioFile(temp_filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text, None
    except sr.UnknownValueError:
        return None, "Could not understand audio."
    except sr.RequestError:
        return None, "API connection error."
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        os.remove(temp_filename)
