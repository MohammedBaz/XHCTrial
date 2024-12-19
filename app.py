# app.py
import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("ChatGPT-like clone")

# Initialize session state for messages and model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"  # Default model

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input and API response
if prompt := st.chat_input("What is up?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant's response by calling the OpenAI model via model.py
    response_stream = get_openai_response(st.session_state.messages, model=st.session_state["openai_model"])

    # Process the response from the model and display
    if response_stream:
        response_content = ""
        for chunk in response_stream:
            if chunk.get("choices"):
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                response_content += content
                st.write(content)  # Display the response as it streams
        # Once streaming is done, append the full response to messages
        st.session_state.messages.append({"role": "assistant", "content": response_content})
