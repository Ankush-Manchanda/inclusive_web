# 🌐 InclusiveWeb: Accessibility Suite

InclusiveWeb is a Streamlit-based application that empowers accessibility through real-time subtitles, text-to-speech, and language translation. This tool is designed especially for differently-abled users — including those with hearing, speech, or language barriers — offering a more inclusive digital experience.

---

## 🚀 Features

### 1️⃣ Real-Time Subtitle Generator
- 🎥 **Upload** audio or video files to transcribe subtitles.
- 🎙️ **Record** video/audio using webcam (manual upload via external tools).
- 📷 **Real-Time Transcription** using live webcam + microphone.
- 📄 Subtitles are displayed in real time in a transcript box.

### 2️⃣ Text-to-Speech (TTS)
- 📝 **Text to Speech**: Type any text and hear it spoken aloud.
- 💬 **Real-Time Speak While Typing**: The system speaks the text as you type.
- 🌐 **Multilingual Output Support**: Output voice supports languages like Hindi, Tamil, Bengali, Marathi, and more.
- 🧠 **Offline + Online TTS Engines**:
  - Uses `Google Cloud TTS` (online with credentials)
  - Falls back to `pyttsx3` if offline

### 3️⃣ Text Translator
- 🌍 Translate typed or spoken text into multiple Indian and international languages.
- 💡 Real-time text translation as the user types.
- 📘 Uses `googletrans` for fast and free translation.

---

## 🛠️ Technology Stack

| Layer            | Technology Used                             |
|------------------|----------------------------------------------|
| Frontend UI      | `Streamlit`                                  |
| Audio Processing | `speechrecognition`, `pydub`, `ffmpeg`       |
| TTS              | `pyttsx3` (offline), `Google Cloud TTS`      |
| Translation      | `googletrans`                                |
| Webcam Streaming | `streamlit-webrtc`                           |
| Audio Playback   | `pygame`                                     |

---

## 🧩 Project Structure

```
InclusiveWeb/
│
├── app.py                    # Main Streamlit app
├── utils/
│   ├── text_to_speech.py     # Text-to-speech handler
│   ├── speech_to_text.py     # Speech recognition logic
│   └── translator.py         # Text translation logic
│
├── requirements.txt          # All required dependencies
├── config.toml               # Streamlit app config (optional)
├── README.md                 # This file
└── google_key.json           # Google Cloud credentials (keep safe!)
```

---

## 🔐 Google Cloud TTS Setup (Optional for Online Use)

To enable Google TTS:
1. Create a project at https://console.cloud.google.com/
2. Enable **Text-to-Speech API**
3. Create **Service Account Key (JSON)** and download
4. Place the file in the root folder as `google_key.json`
5. Set environment variable:

```bash
set GOOGLE_APPLICATION_CREDENTIALS=google_key.json   # Windows
# or
export GOOGLE_APPLICATION_CREDENTIALS=google_key.json # macOS/Linux
```

---

## 🧪 Installation & Running Locally

1. Clone the repo:
```bash
git clone https://github.com/yourusername/InclusiveWeb.git
cd InclusiveWeb
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

---

## ✅ Requirements (requirements.txt)

```txt
streamlit
streamlit-webrtc
googletrans==4.0.0rc1
speechrecognition
pydub
pyttsx3
pygame
av
numpy
ffmpeg-python
google-cloud-texttospeech
```

---

## 💡 Future Enhancements

- 🖼️ Sign language integration
- 👀 OCR for extracting text from images
- 📶 Progressive Web App (PWA) support for offline mode

---

## 👤 Author

**Ankush Manchanda , Anjali**

📧 [ankushmanchanda111@gmail.com](mailto:ankushmanchanda111@gmail.com)
🔗 [GitHub](https://github.com/Ankush-Manchanda)
📧[007anjalichauhan@gmail.com](mailto:007anjalichauhan@gmail.com)
🔗[GitHub](https://github.com/Anjali-codehub)
---

## 📄 License

This project is licensed for educational and non-commercial use only.

