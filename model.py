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

#def get_gemini_response(question, prompt, df):
#    model = genai.GenerativeModel(imports.MODEL_NAME)

 #   # Use Gemini to interpret the question and generate the response
 #   response = model.generate_content([prompt[0], question, str(df)])  # Include the DataFrame in the context
 #   return response.text

# model.py

# ... (rest of your model.py code) ...

def get_gemini_response(question, prompt, df):
    model = genai.GenerativeModel(imports.MODEL_NAME)

    # Use Gemini to interpret the question and generate the response
    response = model.generate_content([prompt[0], question, str(df)])

    # Extract the answer from the response
    answer = extract_answer(response.text)  # You'll need to implement this function

    # If the answer is a number, try to make it more conversational
    if answer.isdigit():
        try:
            # Convert the answer to an integer
            answer_int = int(answer)

            # Example: If the question is about the number of hospitals
            if "how many hospitals" in question.lower():
                # Get the distribution of hospitals by district
                district_counts = df[df["Type"] == "Hospital"]["District"].value_counts()
                district_info = ", ".join([f"{count} in {district}" for district, count in district_counts.items()])
                
                # Formulate the conversational response
                answer = f"There are {answer_int} hospitals in Taif. {district_info}."
                answer += " Do you like to get Beds number or waiting time?"

            # Add more conditions for other types of questions if needed

        except ValueError:
            pass  # If the answer is not a valid integer, keep the original response

    return answer
