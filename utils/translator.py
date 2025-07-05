from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang='en'):
    text = text.strip()
    if not text:
        return "⚠️ Please enter some text to translate."

    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return f"Translation error: {e}"
