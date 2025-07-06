import os
import cv2
import tempfile
import threading
import speech_recognition as sr
from moviepy import VideoFileClip, AudioFileClip

# Transcribe audio file using Google Speech Recognition
def transcribe_audio(path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API unavailable"

# Save uploaded file temporarily
def save_temp_file(uploaded_file):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1])
    temp.write(uploaded_file.read())
    temp.close()
    return temp.name

# Extract audio from video using moviepy
def extract_audio(video_path):
    audio_path = tempfile.mktemp(suffix=".wav")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)
    return audio_path

# Transcribe uploaded file (audio/video)
def transcribe_uploaded_file(uploaded_file):
    temp_path = save_temp_file(uploaded_file)
    ext = os.path.splitext(temp_path)[-1].lower()

    if ext in [".mp3", ".wav", ".m4a"]:
        return transcribe_audio(temp_path)
    elif ext in [".mp4", ".mov", ".avi"]:
        audio_path = extract_audio(temp_path)
        return transcribe_audio(audio_path)
    else:
        return "Unsupported file type"

# Real-time transcription with webcam and mic
def transcribe_realtime(callback=None):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Unable to access webcam")
        return

    stop_flag = threading.Event()

    def listen_and_transcribe():
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            while not stop_flag.is_set():
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                    text = recognizer.recognize_google(audio)
                    if callback:
                        callback(text)
                    else:
                        print(f"🗣️ {text}")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    if callback:
                        callback("[Unclear audio]")
                except sr.RequestError:
                    if callback:
                        callback("[API error]")
                except Exception as e:
                    if callback:
                        callback(f"[Error: {e}]")
                    break

    listener_thread = threading.Thread(target=listen_and_transcribe)
    listener_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("🔴 Live Webcam - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            stop_flag.set()
            break

    cap.release()
    cv2.destroyAllWindows()
    listener_thread.join()
