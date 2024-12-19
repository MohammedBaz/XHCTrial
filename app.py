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
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "how are you"}
  ]
)
st.write(completion.choices[0].message);
