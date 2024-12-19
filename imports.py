import streamlit as st
import pandas as pd
import google.generativeai as genai

# Access the API key from Streamlit secrets
API_KEY = st.secrets["GeminiKey"]

# Configure Genai Key
genai.configure(api_key=API_KEY)

# Gemini model settings
MODEL_NAME = "gemini-pro"

# Load the DataFrame
df = pd.read_csv("data/healthcare_data.csv")

# Import from the correct location
from model import get_gemini_response
