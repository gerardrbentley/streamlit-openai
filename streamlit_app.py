import uuid

import streamlit as st
from st_paywall import add_auth
from simpleaichat import AIChat
import pandas as pd

SESSION_ID = "session_id"
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
PRIME = "Let me think...\n"

st.set_page_config(
    page_title="Streamlit + OpenAI Apps",
    page_icon="🕹",
    initial_sidebar_state="collapsed",
)
st.header("Streamlit + OpenAI App 🎈🤖")

add_auth(required=False)

if not st.session_state.get('user_subscribed'):
    st.warning("""\
# Sign In On the Left

Due to API costs associated with running this app, you must subscribe for a low cost.
""")
    st.stop()
else:
    st.info("""\
Download this chat from the left sidebar
""")

@st.cache_resource
def get_ai() -> AIChat:
    ai = AIChat(
        prime=PRIME,
        console=False,
        model="gpt-3.5-turbo",
    )
    return ai


ai = get_ai()
# Initialize chat history
if SESSION_ID not in st.session_state:
    session_id = uuid.uuid4()
    st.session_state[SESSION_ID] = session_id
    ai.new_session(id=session_id)
else:
    session_id = st.session_state[SESSION_ID]

ai_session = ai.get_session(session_id)

# Display chat messages from history on app rerun
for message in ai_session.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

# React to user input
if prompt := st.chat_input("What else...?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

if prompt is None:
    st.stop()

# Display assistant response in chat message container
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    for chunk in ai.stream(
        id=session_id,
        prompt=prompt,
        system=DEFAULT_SYSTEM_PROMPT,
        params={"max_tokens": 150},
        save_messages=True,
    ):
        full_response += chunk["delta"]
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(chunk["response"])

df = pd.DataFrame([{'role': message.role, 'content': message.content}for message in ai_session.messages])
with st.sidebar.expander('Raw Chat Data'):
    st.sidebar.info("""Copy all entries to excel: 

- Click one cell
- Select all (`ctrl + a`)
- Copy (`ctrl + c`)
- Paste in Excel (`ctrl + v`)

Macs use `cmd` instead of `ctrl` 
""")
    st.sidebar.dataframe(df)

def prep_download(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="Download Conversation as CSV",
    data=prep_download(df),
    file_name='chatgpt_conversation.csv',
    mime='text/csv',
    help="This format of tab separated column values is suitable for copying into excel"
)