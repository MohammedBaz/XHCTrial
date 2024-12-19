# model.py
from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OpenAIKey"]["api_key"])

# Function to generate model response based on messages
def get_openai_response(messages, model="gpt-3.5-turbo"):
    try:
        # Making a call to OpenAI's chat completions API
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None
