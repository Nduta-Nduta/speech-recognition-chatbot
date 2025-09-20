import streamlit as st
import speech_recognition as sr
import datetime

# ------------------------
# Helper Functions
# ------------------------
def transcribe_speech(api="google", language="en-US", paused=False):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if paused:
                return "⏸️ Recognition is paused."

            st.info("🎙️ Listening... Speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            if api == "google":
                return recognizer.recognize_google(audio, language=language)
            elif api == "sphinx":
                return recognizer.recognize_sphinx(audio, language=language)
            else:
                return "❌ Unknown API selected."

    except KeyboardInterrupt:
        return "⚠️ Recording stopped by user."
    except sr.WaitTimeoutError:
        return "⌛ No speech detected (timeout)."
    except sr.UnknownValueError:
        return "❌ Could not understand audio."
    except sr.RequestError as e:
        return f"⚠️ API request failed: {e}"
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"

def save_transcription(text, filename="transcriptions.txt"):
    if not text or text.startswith(("❌", "⚠️", "⏸️")):
        return "⚠️ Nothing valid to save."
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {text}\n")
    return f"✅ Saved transcription to {filename}"

# ------------------------
# Streamlit UI
# ------------------------
st.title("🎤 Safe Speech Recognition App")

# API Selection
api_choice = st.selectbox("Select API:", ["google", "sphinx"])
language_choice = st.text_input("Language code:", "en-US")

# Pause/Resume
if "paused" not in st.session_state:
    st.session_state.paused = False

if st.button("⏸️ Pause" if not st.session_state.paused else "▶️ Resume"):
    st.session_state.paused = not st.session_state.paused

# Record & Transcribe
if st.button("🎙️ Start Recording"):
    try:
        text = transcribe_speech(api=api_choice, language=language_choice, paused=st.session_state.paused)
        st.write(f"📝 **Result:** {text}")

        if text and not text.startswith(("❌", "⚠️", "⏸️")):
            if st.button("💾 Save Transcription"):
                msg = save_transcription(text)
                st.success(msg)

    except KeyboardInterrupt:
        st.warning("⚠️ Recording interrupted by user. Exiting gracefully.")


