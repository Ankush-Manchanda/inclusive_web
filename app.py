import streamlit as st
import tempfile
import threading
from googletrans import Translator
from utils.text_to_speech import speak_text
from utils.speech_to_text import transcribe_uploaded_file, transcribe_realtime

# Page config
st.set_page_config(page_title="InclusiveWeb", layout="centered")
st.title("🌐 InclusiveWeb: Accessibility Suite")

# Session states
if "realtime_transcript" not in st.session_state:
    st.session_state["realtime_transcript"] = ""
if "translated_text" not in st.session_state:
    st.session_state["translated_text"] = ""
if "live_input" not in st.session_state:
    st.session_state["live_input"] = ""
if "tab_index" not in st.session_state:
    st.session_state["tab_index"] = 0
if "trigger_speak" not in st.session_state:
    st.session_state["trigger_speak"] = False
if "trigger_translate" not in st.session_state:
    st.session_state["trigger_translate"] = False

# 🎙️ VOICE COMMAND LOGIC
def listen_command():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎧 Listening for command..."):
            try:
                audio = recognizer.listen(source, timeout=4)
                command = recognizer.recognize_google(audio).lower()
                return command
            except sr.UnknownValueError:
                st.error("😕 Could not understand audio")
            except sr.WaitTimeoutError:
                st.warning("⌛ No input detected")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    return ""

st.sidebar.markdown("### 🎙️ Voice Assistant")
if st.sidebar.button("🎧 Activate Voice Command"):
    command = listen_command()
    st.sidebar.success(f"✅ Recognized: {command}")

    if "subtitle" in command:
        st.session_state["tab_index"] = 0
    elif "speech" in command or "text to speech" in command:
        st.session_state["tab_index"] = 1
    elif "translator" in command or "translate" in command:
        st.session_state["tab_index"] = 2
    elif "clear" in command:
        st.session_state["tts_text_input"] = ""
        st.session_state["translated_text"] = ""
        st.session_state["realtime_transcript"] = ""
        st.success("Cleared all inputs.")
    elif "speak" in command:
        st.session_state["trigger_speak"] = True
    elif "translate now" in command or "do translate" in command:
        st.session_state["trigger_translate"] = True
    else:
        st.info("🤖 Command not matched to any action.")

# Tabs based on session state
tabs = st.tabs([
    "📝 Real-Time Subtitle Generator",
    "🔊 Text to Speech",
    "🌍 Text Translator"
])

# --- TAB 1: Subtitle Generator ---
with tabs[0]:
    st.header("🎤 Real-Time Subtitle Generator")
    option = st.radio("Choose input method:", [
        "📁 Upload File", "📷 Real-Time Transcription"])

    if option == "📁 Upload File":
        uploaded_file = st.file_uploader("Upload an audio/video file", type=["mp3", "wav", "m4a", "mp4"])
        if uploaded_file:
            st.audio(uploaded_file)
            if st.button("▶️ Start Transcription"):
                with st.spinner("Transcribing file..."):
                    text = transcribe_uploaded_file(uploaded_file)
                    st.session_state["realtime_transcript"] = text

    elif option == "📷 Real-Time Transcription":
        def update_transcript(text):
            st.session_state["realtime_transcript"] += f"{text}\n"

        if st.button("▶️ Start Transcription"):
            st.info("Using webcam and mic to generate live subtitles. Press 'Q' to quit the video stream.")
            threading.Thread(target=transcribe_realtime, args=(update_transcript,), daemon=True).start()

    st.subheader("Subtitles")
    st.text_area("Transcript", value=st.session_state["realtime_transcript"], height=250, key="subtitle_box")
    if st.button("🧹 Clear"):
        st.session_state["realtime_transcript"] = ""

# --- TAB 2: Text to Speech ---
with tabs[1]:
    st.header("🔊 Text to Speech")
    tts_mode = st.radio("Choose Mode:", [
        "📝 Text to Speech", "💬 Real-Time Speak While Typing"])

    lang_map = {
        "English": "en-US", "Hindi": "hi-IN", "French": "fr-FR", "Spanish": "es-ES",
        "German": "de-DE", "Tamil": "ta-IN", "Gujarati": "gu-IN", "Bengali": "bn-IN", "Marathi": "mr-IN"
    }

    output_lang = st.selectbox("🎤 Output Voice Language", list(lang_map.keys()), key="tts_output_lang")
    output_lang_code = lang_map[output_lang]

    tts_input = st.text_area("Enter text to speak", key="tts_text_input")

    if st.button("🔊 Speak") or st.session_state.get("trigger_speak"):
        if tts_input.strip():
            audio_bytes = speak_text(tts_input, lang=output_lang_code)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
        else:
            st.warning("⚠️ Please enter some text.")
        st.session_state["trigger_speak"] = False

    if tts_mode == "💬 Real-Time Speak While Typing":
        rts_input = st.text_input("Type and press Enter to speak", key="tts_real_input")
        if rts_input.strip():
            audio_bytes = speak_text(rts_input.strip(), lang=output_lang_code)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

# --- TAB 3: Text Translator ---
with tabs[2]:
    st.header("🌍 Text Translator")

    lang_map = {
        "English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es",
        "German": "de", "Tamil": "ta", "Gujarati": "gu", "Bengali": "bn", "Marathi": "mr"
    }

    selected_lang = st.selectbox("Translate to:", list(lang_map.keys()))
    lang_code = lang_map[selected_lang]

    trans_mode = st.radio("Choose translation mode:", [
        "📄 Translate Text", "💬 Real-Time Text Translation"])

    if trans_mode == "📄 Translate Text":
        text_to_translate = st.text_area("Enter text to translate")
        if st.button("Translate") or st.session_state.get("trigger_translate"):
            from utils.translator import translate_text
            translated = translate_text(text_to_translate, target_lang=lang_code)
            st.session_state["translated_text"] = translated
            st.success("Translated Text:")
            st.text_area("Translation Output", translated, height=150)
            st.session_state["trigger_translate"] = False

    elif trans_mode == "💬 Real-Time Text Translation":
        user_input = st.text_input("Type here and press Enter to translate")
        if user_input:
            from utils.translator import translate_text
            translated = translate_text(user_input, target_lang=lang_code)
            st.session_state["translated_text"] = translated

    st.text_area("Live Translation Output", st.session_state["translated_text"], height=150)
