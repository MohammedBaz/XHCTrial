import streamlit as st
import pandas as pd
import re
from model import get_openai_response

# Load the healthcare dataset
@st.cache_data
def load_data():
    return pd.read_csv("healthcare_data.csv")

data = load_data()

# Streamlit app layout
st.title("Healthcare Facility Data")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for a new message
if user_input := st.chat_input("Ask a question about the healthcare data:"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Function to identify the intent based on keywords
    def identify_intent(query):
        if re.search(r'\b(hospital|clinic|polyclinic)\b', query, re.IGNORECASE):
            return "facility_names"
        elif re.search(r'\b(doctors|nurses)\b', query, re.IGNORECASE):
            return "staff_count"
        elif re.search(r'\b(satisfaction|patient satisfaction)\b', query, re.IGNORECASE):
            return "avg_satisfaction"
        elif re.search(r'\b(waiting time)\b', query, re.IGNORECASE):
            return "avg_waiting_time"
        elif re.search(r'\b(beds|occupancy)\b', query, re.IGNORECASE):
            return "total_beds"
        else:
            return "openai_query"

    # Determine the intent based on user input
    intent = identify_intent(user_input)

    # Handle different intents
    if intent == "facility_names":
        # Query for the names of all facilities
        facility_names = data["Facility Name"].tolist()
        assistant_response = f"The facilities are: {', '.join(facility_names)}."

    elif intent == "staff_count":
        # Query the total number of doctors or nurses
        if "doctor" in user_input.lower():
            doctor_count = data["Doctors"].sum()
            assistant_response = f"The total number of doctors across all facilities is {doctor_count}."
        elif "nurse" in user_input.lower():
            nurse_count = data["Nurses"].sum()
            assistant_response = f"The total number of nurses across all facilities is {nurse_count}."
        else:
            assistant_response = "Please specify whether you're asking for the number of doctors or nurses."

    elif intent == "avg_satisfaction":
        # Query the average patient satisfaction
        avg_satisfaction = data["PatientSatisfaction"].mean()
        assistant_response = f"The average patient satisfaction across all facilities is {avg_satisfaction:.2f}."

    elif intent == "avg_waiting_time":
        # Query the average waiting time
        avg_waiting_time = data["WaitingTime"].mean()
        assistant_response = f"The average waiting time across all facilities is {avg_waiting_time:.2f}."

    elif intent == "total_beds":
        # Query the total number of beds
        total_beds = data["Beds"].sum()
        assistant_response = f"The total number of beds across all facilities is {total_beds}."

    else:
        # For complex or general queries, use OpenAI to get an answer
        assistant_message = get_openai_response(st.session_state.messages)
        if assistant_message:
            assistant_response = assistant_message.content
        else:
            assistant_response = "Sorry, I could not understand your question."

    # Append assistant's response to session state and display it
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
