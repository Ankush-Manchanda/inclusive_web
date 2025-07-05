import os
import tempfile
import pyttsx3

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False


def custom_voice_name(lang_code):
    voice_map = {
        "en-US": "en-US-Wavenet-F",
        "hi-IN": "hi-IN-Wavenet-D",
        "ta-IN": "ta-IN-Wavenet-A",
        "gu-IN": "gu-IN-Wavenet-A",
        "bn-IN": "bn-IN-Wavenet-A",
        "mr-IN": "mr-IN-Wavenet-A",
        "fr-FR": "fr-FR-Wavenet-B",
        "es-ES": "es-ES-Wavenet-B",
    }
    return voice_map.get(lang_code, "")


def speak_text(text, lang="en-US"):
    if not text.strip():
        print("⚠️ Empty text provided to speak.")
        return

    # 1️⃣ Try Google TTS if available
    if GOOGLE_TTS_AVAILABLE and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=lang,
                name=custom_voice_name(lang),
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            print(f"🔊 Using Google TTS (language: {lang})")
            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                out.write(response.audio_content)
                temp_file_path = out.name

            # Play using pygame
            import pygame
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            # Wait until done playing
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.quit()
            os.remove(temp_file_path)
            return
        except Exception as e:
            print(f"⚠️ Google TTS failed: {e}")

    # 2️⃣ Fallback to pyttsx3
    print("🔊 Falling back to pyttsx3...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Attempt to match language with available voice
        selected_voice = None
        for voice in voices:
            if lang.split('-')[0] in voice.languages[0].decode('utf-8').lower():
                selected_voice = voice.id
                break

        if selected_voice:
            engine.setProperty('voice', selected_voice)

        engine.setProperty('rate', 170)    # Speed
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ pyttsx3 also failed: {e}")
