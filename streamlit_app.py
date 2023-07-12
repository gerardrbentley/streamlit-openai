import streamlit as st
from st_paywall import add_auth
from simpleaichat import AIChat

CHAT_HISTORY = "chat_history"
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
PRIME = "Let me think...\n"

st.set_page_config(
    page_title="Streamlit + OpenAI Apps",
    page_icon="🕹",
    initial_sidebar_state="collapsed",
)
add_auth(required=False)

st.header("Streamlit + OpenAI App 🎈🤖")

# Initialize chat history
if CHAT_HISTORY not in st.session_state:
    st.session_state[CHAT_HISTORY] = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT}
    ]

def get_system_message() -> str:
    return st.session_state[CHAT_HISTORY][0]["content"]

# Display chat messages from history on app rerun
for message in st.session_state[CHAT_HISTORY]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What else...?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state[CHAT_HISTORY].append({"role": "user", "content": prompt})

if prompt is None:
    st.stop()

# Display assistant response in chat message container
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    ai = AIChat(
        prime=PRIME, 
        console=False,
        model= "gpt-3.5-turbo",
        system=DEFAULT_SYSTEM_PROMPT,
        messages=st.session_state[CHAT_HISTORY],
        params={"max_tokens": 300},
        save_messages=False,
    )
    for chunk in ai.stream(prompt=prompt):
        full_response += chunk["delta"]
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(chunk["response"])

# Add assistant response to chat history
st.session_state[CHAT_HISTORY].append({"role": "assistant", "content": full_response})