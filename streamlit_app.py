import openai
import streamlit as st
from streamlit_chat import message, AvatarStyle

openai.api_key = st.secrets["api_key"]

CHAT_HISTORY = "chat_history"
CHAT_INPUT = "chat_input"

if CHAT_HISTORY not in st.session_state:
    st.session_state[CHAT_HISTORY] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

def submit_chat():
    try:
        chat_input = st.session_state[CHAT_INPUT]
        st.session_state[CHAT_HISTORY].append({"role": "user", "content": chat_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=st.session_state[CHAT_HISTORY]
        )
        st.session_state[CHAT_HISTORY].append(
            {
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            }
        )
    except Exception as e:
        print(repr(e))
        st.error("Could not fetch AI Response properly")

for i, chat in enumerate(st.session_state[CHAT_HISTORY]):
    if chat["role"] == "assistant":
        message(chat["content"], key=str(i))
    elif chat["role"] == "user":
        message(chat["content"], is_user=True, key=str(i))
    elif chat["role"] == "system":
        message(chat["content"], is_user=True, avatar_style="jdenticon", key=str(i))


with st.form("chat_input", True):
    st.text_area("Message to send:", key=CHAT_INPUT)
    st.form_submit_button("Send Chat", on_click=submit_chat)
