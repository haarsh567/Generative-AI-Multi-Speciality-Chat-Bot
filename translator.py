import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from translate import Translator

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar contents
with st.sidebar:
    st.title('🦜️Translator- Chatbot💬')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilised to create::

    - [streamlit](https://streamlit.io/)
    - [Gemini](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)

    ## About me:

    - [Linkedin](https://www.linkedin.com/in/harsh-gupta-110074283/)
    
    ''')

    st.write('💡All about Gemini exploration created by Harsh Gupta🤗')

# List available models
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Streamlit app
st.title("Audio Based Chatbot With Translator💬")

# Model selection
selected_model = st.selectbox("Select a Generative Model", models)

# Real-time audio input and speech-to-text conversion
fs = 16000  # Sample rate
duration = 5  # Recording duration in seconds

# Check if the user has submitted audio
submitted = st.button("Speak and Submit")

# Initialize transcription variable
transcribed_text = ""

# Initialize session_state
if 'lang_code' not in st.session_state:
    st.session_state.lang_code = "en"  # Default language code is English
    st.session_state.translated_result = None  # Initialize translated result

if submitted:
    st.write("Speak now...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait for recording to finish

    # Save the recorded audio to a temporary file
    temp_file = "temp.wav"
    sf.write(temp_file, recording, fs)

    # Speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_file) as source:
        audio = recognizer.record(source)
        transcribed_text = recognizer.recognize_google(audio)

    # Display transcribed text
    st.subheader("Transcribed Text:")
    st.write(transcribed_text)

    # Process the transcribed text 
    processed_text = transcribed_text.upper()  
    # Display processed text
    st.subheader("Processed Text:")
    st.write(processed_text)

    # Generate content using Gemini
    model = genai.GenerativeModel(selected_model)
    response = model.generate_content(processed_text)  

    # Display generated content
    st.subheader("Generated Content:")
    st.write(response.text)

    # Translation step
    st.subheader("Translation:")
    dest_lang = st.selectbox("Select destination language", {"Tamil", "Hindi", "Telugu", "Punjabi", "German", "English", "French"})
    if dest_lang:
        language_codes = {
            "Tamil": "ta",
            "Hindi": "hi",
            "Telugu": "te",
            "Punjabi": "pa",
            "German": "de",
            "English": "en",
            "French": "fr",
        }
        dest_lang_code = language_codes.get(dest_lang)

        # Update session_state with the selected language code
        st.session_state.lang_code = dest_lang_code

        # Use Translator without st.cache
        try:
            translator = Translator(to_lang=dest_lang_code)
            translation = translator.translate(response.text)
            st.session_state.translated_result = translation
            st.write(f"**Translated Answer ({dest_lang}):** {translation}")
        except Exception as e:
            st.error(f"An error occurred during translation: {str(e)}")

    # Clean up the temporary audio file
    os.remove(temp_file)
