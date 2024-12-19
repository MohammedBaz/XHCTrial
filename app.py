import openai
import streamlit as st
import pandas as pd

# Load the CSV file (make sure this file is accessible in your Streamlit Cloud project)
df = pd.read_csv("healthcare_data.csv")

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OpenAIKey"]["api_key"]

# Streamlit app title
st.title("Healthcare Facility Data Query")

# User input for the question
user_question = st.text_input("Ask a question about the healthcare data:")

# Function to call OpenAI's API and get a response based on the user's query and CSV data
def get_openai_answer(question, data):
    context = f"Here is the healthcare data:\n\n{data}\n\nAnswer the question: {question}"
    
    try:
        # Use the completions endpoint with the new method
        response = openai.Completion.create(
            model="gpt-4",  # Use the correct model, e.g., "gpt-4" or another version
            prompt=context,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    
    except Exception as e:  # General exception handling
        st.error(f"Error: {str(e)}")  # Log the error message for troubleshooting
        return f"Error: {str(e)}"

# Displaying the answer when a user submits a question
if user_question:
    # Convert dataframe to string
    data_str = df.to_string(index=False)
    
    # Get the response from OpenAI
    answer = get_openai_answer(user_question, data_str)
    
    # Display the result
    st.write(f"Answer: {answer}")
