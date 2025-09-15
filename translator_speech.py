# translator_speech.py
import platform
import os
from googletrans import Translator
from gtts import gTTS

_translator = Translator()

def translate_text(text, dest_lang="hi"):
    try:
        res = _translator.translate(text, dest=dest_lang)
        return res.text
    except Exception:
        # fallback to original text
        return text

def text_to_speech(text, lang="hi", filename="advisory.mp3", play=False):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    if play:
        system = platform.system()
        if system == "Windows":
            os.startfile(filename)
        elif system == "Darwin":
            os.system(f"afplay {filename} &")
        else:
            os.system(f"mpg123 {filename} >/dev/null 2>&1 &")
    return filename
