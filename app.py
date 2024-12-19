import streamlit as st
import pandas as pd
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

    # Check if the user query is data-related
    if "doctor" in user_input.lower():
        # Query the number of doctors across all facilities
        doctor_count = data["Doctors"].sum()
        assistant_response = f"The total number of doctors across all facilities is {doctor_count}."
    elif "nurse" in user_input.lower():
        # Query the number of nurses across all facilities
        nurse_count = data["Nurses"].sum()
        assistant_response = f"The total number of nurses across all facilities is {nurse_count}."
    elif "satisfaction" in user_input.lower():
        # Query the average patient satisfaction
        avg_satisfaction = data["PatientSatisfaction"].mean()
        assistant_response = f"The average patient satisfaction is {avg_satisfaction:.2f}."
    elif "waiting time" in user_input.lower():
        # Query the average waiting time
        avg_waiting_time = data["WaitingTime"].mean()
        assistant_response = f"The average waiting time across all facilities is {avg_waiting_time:.2f}."
    elif "beds" in user_input.lower():
        # Query the total number of beds
        total_beds = data["Beds"].sum()
        assistant_response = f"The total number of beds across all facilities is {total_beds}."
    elif "facility type" in user_input.lower():
        # Query the unique types of facilities
        facility_types = data["Type"].unique()
        assistant_response = f"The types of facilities are: {', '.join(facility_types)}."
    else:
        # For other queries, use OpenAI to get an answer
        assistant_message = get_openai_response(st.session_state.messages)
        if assistant_message:
            assistant_response = assistant_message.content
        else:
            assistant_response = "Failed to fetch response from OpenAI."

    # Append assistant's response to session state and display it
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
