import streamlit as st
from model import get_openai_response

# Streamlit app layout
st.title("ChatGPT-like Clone")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the chat history

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for a new message
if user_input := st.chat_input("Ask me something:"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    with st.chat_message("assistant"):
        response_container = st.empty()  # Placeholder for dynamic updates
        full_response = ""

        # Fetch the response from the OpenAI model as a stream
        response_stream = get_openai_response(st.session_state.messages)
        if response_stream:  # Check if the response stream is valid
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.get("content", "")
                    full_response += content
                    response_container.markdown(full_response)  # Update dynamically
        else:
            st.error("Failed to fetch response from the OpenAI API.")

        # Save the assistant's response to session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
