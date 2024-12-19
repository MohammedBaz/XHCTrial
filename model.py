import google.generativeai as genai
import pandas as pd
import imports  

# Define Your Prompt
prompt = [
    """
    You are an AI chatbot designed to answer questions about Taif medical institutions.
    You have access to a Pandas DataFrame with the following columns:

    Facility Name, District, Type, Beds, Speciality, Doctors, Nurses, Outpatients, Inpatients, WaitingTime, OccupancyRate, PatientSatisfaction.

    Instructions:
    - If the user greets you or asks a general question, respond in a friendly and professional manner.
    - If the user asks a specific question about Taif medical institutions that can be answered using the data in the DataFrame, call the function `get_data_from_df(question)` to retrieve the answer.
    - If the user asks a question unrelated to Taif medical institutions or that cannot be answered using the data, say "This question cannot be answered using the Taif medical institutions data."

    Please provide ONLY the answer to the question as your output.
    """
]



def extract_answer(response_text):
    # Assuming the answer is the last line of the response
    return response_text.strip().split("\n")[-1]

def get_gemini_response(question, prompt, df):
    model = genai.GenerativeModel(imports.MODEL_NAME)

    # Use Gemini to interpret the question and generate the response
    response = model.generate_content([prompt[0], question, str(df)])

    # Extract the answer from the response
    answer = extract_answer(response.text)

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
