# app.py
import nltk
import streamlit as st
import speech_recognition as sr
import random
import string

# Download necessary nltk resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

# ------------------------
# Chatbot Preprocessing
# ------------------------
# Load a sample corpus or text file
with open("chatbot_corpus.txt", "r", errors="ignore") as f:
    raw = f.read().lower()

# Tokenization
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Lemmatizer
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# ------------------------
# Simple Chatbot Response
# ------------------------
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["hi", "hey", "hello", "I am glad you're talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def chatbot_response(user_input):
    user_input = user_input.lower()
    if greeting(user_input) is not None:
        return greeting(user_input)
    else:
        return "I'm not sure I understand you, but I'm learning!"

# ------------------------
# Speech Recognition
# ------------------------
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand your speech."
    except sr.RequestError:
        return "Sorry, speech service is unavailable right now."

# ------------------------
# Streamlit App
# ------------------------
st.title("🗣️ Speech-Enabled Chatbot")
st.write("Talk to me using text or your microphone!")

# Text input
user_text = st.text_input("💬 Type your message here:")

# Speech input
if st.button("🎤 Use Voice Input"):
    user_text = speech_to_text()
    st.write(f"**You said:** {user_text}")

# Generate response
if user_text:
    response = chatbot_response(user_text)
    st.write(f"🤖 **Chatbot:** {response}")

