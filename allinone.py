import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import PIL.Image

# Function definitions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GooglePalmEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    llm = GooglePalm()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain

def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write("Human: ", message.content)
        else:
            st.write("Bot: ", message.content)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar contents
with st.sidebar:
    st.title('🦜️ ALL IN ONE Chatbot')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilised to create::

    - [streamlit](https://streamlit.io/)
    - [Gemini](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)
    - [Palm2](https://ai.google/discover/palm2)

    ## About me:

    - [Linkedin](https://www.linkedin.com/in/harsh-gupta-110074283/)
    
    ''')

    add_vertical_space(1)
    st.write('💡All about Gemini and Palm2 exploration created by Harsh Gupta🤗')
    st.write('💡Full credit: Gemini AI🤗')

# List available models
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Streamlit app
st.title(" Vision, Multiple Pdf, Prompt & Audio Based Chatbot")

# Model selection
selected_model = st.selectbox("Select a Generative Model", models)

# Choose processing type
selected_option = st.selectbox("Select Processing Type", ["Text", "Audio"])

# Function to clear session state
def clear_session_state():
    st.session_state.conversation = None
    st.session_state.chatHistory = None

# Clear session state if the user changes the processing type
if st.session_state.get('selected_option') != selected_option:
    clear_session_state()

# Store the current processing type in session state
st.session_state.selected_option = selected_option

# Handle selected processing type
if selected_option == "Text":
    # File uploader for vision model
    if 'generateContent' in genai.get_model(selected_model).supported_generation_methods:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        # Display uploaded image
        if uploaded_file is not None:
            # Read the uploaded image
            img = PIL.Image.open(uploaded_file)

            # Display the uploaded image
            st.subheader("Uploaded Image:")
            st.image(img, caption="Uploaded Image", use_column_width=True)

            # Generate content based on the image
            vision_model = genai.GenerativeModel(selected_model)
            response = vision_model.generate_content(img)

            # Display generated content
            st.subheader("Generated Content:")
            st.write(response.text)
        else:
            # Text input form
            question = st.text_input("Ask a question:")
            submitted = st.button("Submit")

            # Generate content on submission
            if submitted:
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(question)

                # Display question and generated content
                st.subheader("Question:")
                st.write(question)

                st.subheader("Generated Content:")
                st.write(response.text)

elif selected_option == "Audio":
    # Real-time audio input and speech-to-text conversion
    fs = 16000  # Sample rate
    duration = 5  # Recording duration in seconds

    # Check if the user has submitted audio
    submitted = st.button("Speak and Submit")

    # Initialize transcription variable
    transcribed_text = ""

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

        # Clean up the temporary audio file
        os.remove(temp_file)

# Multiple PDF-based chatbot UI
pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
if st.button("Process PDFs"):
    with st.spinner("Processing PDFs"):
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        vector_store = get_vector_store(text_chunks)
        st.session_state.conversation = get_conversational_chain(vector_store)

# User input for PDF-based chatbot
user_question = st.text_input("Ask a Question from the PDF Files")
if user_question:
    user_input(user_question)
