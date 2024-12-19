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
    - If the user asks a question that can be answered using the data in the DataFrame, you MUST analyze the data and provide the answer based on the information in the DataFrame.
    - Do not guess or make up answers. Only provide answers that are directly supported by the data in the DataFrame.
    

    Please provide the answer to the question as your output.
    """
]

def get_gemini_response(question, prompt, df):
    model = genai.GenerativeModel(imports.MODEL_NAME)

    # Use Gemini to interpret the question and generate the response
    response = model.generate_content([prompt[0], question, str(df)])  # Include the DataFrame in the context
    return response.text
