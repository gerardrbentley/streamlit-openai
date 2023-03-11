import logging
from pathlib import Path

import streamlit as st
import openai
import pandas as pd

from interactors import ChatGPTRequest, ChatMessage, SYSTEM
from pocketbase import get_authenticated_user, PocketBaseUser
from initialize_app import st_login

st.set_page_config(
    page_title="ChatGPT Conversation",
    page_icon="🕹",
    initial_sidebar_state="collapsed",
)
authenticated_user = st_login()
st.markdown("<style>" + Path('static/style.css').read_text() + "</style>", unsafe_allow_html=True)

st.header("Streamlit ChatGPT Conversation 🎈🤖")

with st.expander("What's this?"):
    st.write(
        """\
This app allows you to have a conversation with ChatGPT.

The whole chat history will be sent along with each message you send.
This lets you ask the AI about specific parts of its response.

See the [Main Page](/) or [Github Repo](https://github.com/gerardrbentley/streamlit-openai) for more info!

Made with ❤️ by [Gerard Bentley](https://gerardbentley.com)
"""
    )
    st.image("static/chat_demo.gif")

CHAT_HISTORY = "chat_history"
CHAT_INPUT = "chat_input"
response_col, request_col = st.columns(2, gap="large")

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

lines = []
for i, chat in enumerate(st.session_state[CHAT_HISTORY]):
    if chat["role"] == "assistant":
        lines.append('ChatGPT:\n')
        lines.append(chat['content'])
    elif chat["role"] == "user":
        lines.append(f'<p class="from-me" >{authenticated_user.name or authenticated_user.username}: {chat["content"]}</p>')
    elif chat["role"] == "system":
        lines.append(f'<p class="from-me">System Prompt: {chat["content"]}</p>')

st.write('<div class="imessage">' + '\n'.join(lines) + '</div>', unsafe_allow_html=True)

if not authenticated_user:
    st.stop()

with st.form("chat_input", True):
    st.text_area("Message to send:", key=CHAT_INPUT)
    st.form_submit_button("Send Chat", on_click=submit_chat)

def prep_download() -> bytes:
    df = pd.DataFrame(st.session_state[CHAT_HISTORY])
    return df.to_csv().encode('utf-8')

st.download_button(
    label="Download Conversation as CSV",
    data=prep_download(),
    file_name='chatgpt_conversation.csv',
    mime='text/csv',
    help="This format of tab separated column values is suitable for copying into excel"
)