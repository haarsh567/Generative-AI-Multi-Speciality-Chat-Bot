import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import PIL.Image
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

#sidebar contents

with st.sidebar:
    st.title('🤖A - Generative AI ChatBot')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilised to create::

    - [streamlit](https://streamlit.io/)
    - [Gemini Api](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)



    ## About me:

    - [Linkedin](https://www.linkedin.com/in/harsh-gupta-110074283/)
    
    ''')

    add_vertical_space(4)
    st.write('💡All about Gemini exploration created by Harsh Gupta🤗')

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# List available models
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

