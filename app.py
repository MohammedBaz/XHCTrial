# app.py

from imports import *

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get user input
if prompt := st.chat_input(""):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response using the model
        response = get_gemini_response(prompt, model.prompt, df)

        # Check if the response is a function call
        if response.startswith("get_data_from_df("):
            # Extract the question from the function call
            question_to_answer = response[len("get_data_from_df("):-1]
            
            # Get the answer from the DataFrame
            answer = get_data_from_df(question_to_answer, df)  # Pass the DataFrame to the function
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            # Add assistant message to chat history (answer only)
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    with st.container(key=f"{message['role']}_{i}"):
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Add styling for the chat
st.markdown(
    """
    <style>
    [data-testid="stChatMessage"][data-role="user"] .stChatMessageBox {
        background-color: #f0f0f0;
        border-radius: 10px 10px 10px 0px;
    }
    [data-testid="stChatMessage"][data-role="assistant"] .stChatMessageBox {
        background-color: #eaf7ff;
        border-radius: 10px 10px 0px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
