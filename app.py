import streamlit as st
import openai

# Get the OpenAI API Key from Streamlit's sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")

# Title of the Streamlit app
st.title("💬 Chatbot")

# Initialize session state if not already done
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Process the user input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Set the OpenAI API key
    openai.api_key = openai_api_key
    
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Request a completion from OpenAI's GPT-3.5 or GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use another model, e.g., "gpt-4"
            messages=st.session_state.messages,
            max_tokens=150,
            temperature=0.7
        )
        
        # Get the response message
        msg = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    except Exception as e:
        # Handle general exceptions, which can capture API errors or others
        st.error(f"Error: {str(e)}")
