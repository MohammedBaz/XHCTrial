# model.py

import google.generativeai as genai
import pandas as pd
import imports  # Import the imports module

# Define Your Prompt
prompt = [
    """
    You are an AI chatbot designed to answer questions about Taif medical institutions.
    You have access to a Pandas DataFrame with the following columns:

    Facility Name, District, Type, Beds, Speciality, Doctors, Nurses, Outpatients, Inpatients, WaitingTime, OccupancyRate, PatientSatisfaction.

    Instructions:
    - If the user greets you or asks a general question, respond in a friendly and professional manner.
    - If the user asks a specific question about Taif medical institutions that can be answered using the data in the DataFrame, analyze the data and provide the answer.
    - If the user asks a question unrelated to Taif medical institutions or that cannot be answered using the data, say "This question cannot be answered using the Taif medical institutions data."

    Please provide the answer to the question as your output.
    """
]

def get_gemini_response(question, prompt, df):
    model = genai.GenerativeModel(imports.MODEL_NAME)

    # Use Gemini to interpret the question and generate the response
    response = model.generate_content([prompt[0], question, str(df)])  # Include the DataFrame in the context
    return response.text
