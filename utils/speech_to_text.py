import speech_recognition as sr

def transcribe_audio(file_path, use_partial=False):
    recognizer = sr.Recognizer()
    text_output = ""

    try:
        with sr.AudioFile(file_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            if use_partial:
                print("🔄 Transcribing with partial mode (chunked)...")
                while True:
                    try:
                        audio_data = recognizer.record(source, duration=10)
                        if not audio_data.frame_data:
                            break
                        chunk_text = recognizer.recognize_google(audio_data)
                        text_output += chunk_text + " "
                    except sr.UnknownValueError:
                        text_output += "[Unclear audio] "
                    except sr.RequestError as e:
                        return f"⚠️ API error during transcription: {e}"
                    except Exception as e:
                        break
                return text_output.strip()
            else:
                print("🔄 Transcribing full audio...")
                audio_data = recognizer.record(source)
                text_output = recognizer.recognize_google(audio_data)
                return text_output

    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError as e:
        return f"❌ Speech Recognition API request failed: {e}"
    except FileNotFoundError:
        return "❌ Audio file not found."
    except Exception as e:
        return f"❌ An error occurred: {str(e)}"
