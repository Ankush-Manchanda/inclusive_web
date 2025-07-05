import os
import tempfile
import streamlit as st

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
        st.warning("⚠️ Empty text provided to speak.")
        return

    # ✅ Try Google TTS if available
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

            # Save to temp MP3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                out.write(response.audio_content)
                temp_file_path = out.name

            # Play in Streamlit
            with open(temp_file_path, "rb") as f:
                audio_bytes = f.read()

            os.remove(temp_file_path)
            return audio_bytes


        except Exception as e:
            st.error(f"⚠️ Google TTS failed: {e}")

    # ❌ pyttsx3 not supported in cloud – notify user
    st.error("❌ pyttsx3 fallback not available in web apps. Please upload Google TTS credentials.")
