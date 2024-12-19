import streamlit as st
import openai

# Set your API key
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OpenAIKey"]["api_key"])

st.write(openai.api_key)
# Streamlit app layout
st.title("OpenAI Chat with GPT")

# User input field
user_input = st.text_input("Ask something:", "")

if user_input:
    # Call the OpenAI API for chat completions
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Choose the model you want to use
        messages=[
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    
    # Display the model's response
    assistant_response = response['choices'][0]['message']['content']
    st.write("Assistant's Response:")
    st.write(assistant_response)
