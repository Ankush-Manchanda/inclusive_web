import os
import tempfile
import streamlit as st

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

try:
    import pyttsx3
    LOCAL_TTS_AVAILABLE = True
except ImportError:
    LOCAL_TTS_AVAILABLE = False


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
        st.warning("⚠️ Empty text provided to speak.")
        return None

    # ✅ 1. Try Google TTS if credentials available
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

            st.info(f"🔊 Speaking using Google TTS (Language: {lang})")

            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                out.write(response.audio_content)
                temp_file_path = out.name

            with open(temp_file_path, "rb") as f:
                audio_bytes = f.read()

            os.remove(temp_file_path)
            return audio_bytes

        except Exception as e:
            st.error(f"⚠️ Google TTS failed: {e}")

    # ✅ 2. Try pyttsx3 locally if Google TTS not available
    if LOCAL_TTS_AVAILABLE:
        try:
            # Block pyttsx3 on Streamlit Cloud
            if os.getenv("HOME", "").startswith("/home/adminuser") or os.getenv("STREAMLIT_ENV") == "cloud":
                raise EnvironmentError("pyttsx3 fallback not available in web apps. Please upload Google TTS credentials.")

            st.info("🔊 Speaking using local pyttsx3 engine...")

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selected_voice = None
            for voice in voices:
                try:
                # Some voices might not have languages attribute properly set
                    if hasattr(voice, 'languages') and voice.languages:
                        if lang.split('-')[0] in voice.languages[0].decode('utf-8').lower():
                            selected_voice = voice.id
                        break
                except Exception:
                 continue

            if selected_voice:
                engine.setProperty('voice', selected_voice)

            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            return None  # No audio_bytes needed for local

        except EnvironmentError as ee:
            st.error(f"❌ {ee}")
        except Exception as e:
            st.error(f"❌ pyttsx3 also failed: {e}")

    st.error("❌ No available TTS engine found.")
    return None
