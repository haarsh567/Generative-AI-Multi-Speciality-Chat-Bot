# Generative AI Multi-Speciality Chat Bot

## Overview

This project is a multi-speciality chatbot powered by Generative AI, developed in different phases to showcase various capabilities. The chatbot is built using Streamlit, Google Generative AI, PyPDF2, SpeechRecognition, and other relevant libraries.

## Phases

### Phase 1: Basic Chatbot using Gemini API

- Implemented a basic chatbot using the Gemini API.
- Behaves like a chat-based model using Gemini.
  
  **Libraries Used:**
  - [Streamlit](https://streamlit.io/)
  - [Gemini API](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)

### Phase 2: Generative AI Chatbot for Image Content

- Introduced a generative AI chatbot capable of generating content from images.
- Utilized Google Generative AI models to process and generate content based on uploaded images.
  
  **Libraries Used:**
  - [Streamlit](https://streamlit.io/)
  - [Google Generative AI](https://github.com/googleapis/python-generativeai)
  - [PIL (Pillow)](https://pillow.readthedocs.io/)

### Phase 3: Multi-Functional Chatbot

- Implemented a multi-functional chatbot capable of handling different processing types:
  - Text: Accepts user input and generates content based on prompts.
  - Vision: Processes and generates content from uploaded images.
  - PDF: Processes multiple PDF files, allowing users to ask questions from the content.
  
  **Libraries Used:**
  - [Streamlit](https://streamlit.io/)
  - [PyPDF2](https://pythonhosted.org/PyPDF2/)
  - [Google Generative AI](https://github.com/googleapis/python-generativeai)
  - [PIL (Pillow)](https://pillow.readthedocs.io/)

### Phase 4: Audio-Based Generative AI Chatbot

- Introduced an audio-based chatbot capable of:
  - Real-time audio input.
  - Speech-to-text conversion.
  - Translation of audio content to different languages.
  - Generating responses based on transcribed text.
  
  **Libraries Used:**
  - [Streamlit](https://streamlit.io/)
  - [Sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.2/)
  - [Soundfile](https://pysoundfile.readthedocs.io/en/latest/)
  - [NumPy](https://numpy.org/)
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
  - [Google Generative AI](https://github.com/googleapis/python-generativeai)

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/generative-ai-chatbot.git
   cd generative-ai-chatbot
   Usage
Access the chatbot through the Streamlit web interface.
Choose different processing types and interact with the chatbot.
Upload images, PDF files, or use the audio-based feature for a versatile experience.
Additional Information
For more details about each phase, refer to the respective sections in the codebase.
Connect with the developer on LinkedIn.
Credits
Full credit to Gemini AI for their contributions to the project.
Special thanks to Streamlit for the user interface.
License
This project is licensed under the MIT License - see the LICENSE file for details.
