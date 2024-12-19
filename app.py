import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("ChatGPT-like Clone")

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user prompt
if prompt := st.chat_input("What is up?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant's response
    with st.chat_message("assistant"):
        response_container = st.empty()  # For dynamic updates
        response = ""

        # Get the OpenAI response as a stream
        for chunk in get_openai_response(st.session_state["openai_model"], st.session_state.messages):
            if chunk.choices and chunk.choices[0].delta:
                content = chunk.choices[0].delta.get("content", "")
                response += content
                response_container.markdown(response)  # Dynamically update response
        
        # Save the full response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})
