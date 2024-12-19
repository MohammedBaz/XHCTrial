import streamlit as st
import pandas as pd
import openai

# Load the CSV file
df = pd.read_csv("healthcare_data.csv")

# Set your OpenAI API key
openai.api_key = st.secrets["OpenAIKey"]

# Streamlit app title
st.title("Healthcare Facility Data Query")

# User input for the question
user_question = st.text_input("Ask a question about the healthcare data:")

# Function to call OpenAI's API and get a response based on the user's query and CSV data
def get_openai_answer(question, data):
    context = f"Here is the healthcare data:\n\n{data}\n\nAnswer the question: {question}"
    
    # Use the updated API method for the new version
    response = openai.completions.create(
        model="gpt-4o-mini",  # or gpt-4 if available
        prompt=context,
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()

# Displaying the answer when a user submits a question
if user_question:
    # Convert dataframe to string
    data_str = df.to_string(index=False)
    
    # Get the response from OpenAI
    answer = get_openai_answer(user_question, data_str)
    
    # Display the result
    st.write(f"Answer: {answer}")
