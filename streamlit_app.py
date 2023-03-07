import logging

import streamlit as st
import openai

from interactors import ChatGPTRequest, ChatMessage, SYSTEM
from pocketbase import get_authenticated_user, PocketBaseUser

st.set_page_config(
    page_title="Streamlit + OpenAI Apps",
    page_icon="🕹",
    initial_sidebar_state="collapsed",
)

api_key = st.secrets.get("api_key")
if api_key is None:
    st.error("No api_key in .streamlit/secrets.toml")
    st.stop()
openai.api_key = api_key


st.header("Streamlit + OpenAI App 🎈🤖")

def authenticate_pocketbase() -> PocketBaseUser:
    username = st.session_state.get("pocketbase_username")
    password = st.session_state.get("pocketbase_password")
    try:
        user = get_authenticated_user(username, password)
        st.session_state["user_key"] = user
    except Exception:
        logging.exception("Could not authenticate user")
        st.error("Error Logging In. Try again.")

authenticated_user: PocketBaseUser = st.session_state.get("user_key")
if not authenticated_user:
    with st.form("sign_in", clear_on_submit=True):
        st.text_input("Username", key="pocketbase_username")
        st.text_input("Password",key="pocketbase_password")
        st.form_submit_button("Log In", on_click=authenticate_pocketbase)
    st.warning("Not Logged In. Must Sign In to See Results")
else:
    st.subheader(f"Welcome {authenticated_user.name or authenticated_user.username}!")

with st.expander("What's this?"):
    st.write(
        """\
This is a [Streamlit](https://streamlit.io) 🎈 app that uses the [OpenAI](https://platform.openai.com) API to generate chat responses based on user input.

The app has a sidebar on the left with options for the number of responses, AI temperature, presence penalty, and frequency penalty. These options influence the AI's behavior when generating responses.

To generate AI-based chat responses, you need to enter text in the "ChatGPT input" field and hit the "Submit" button. This text will be used as the start of the conversation, and the AI will generate responses based on it.

The response from the API is then displayed in the app along with the raw response.

The app requires an admin user with a user key provided in the URL to access its features.

If you have an OpenAI API Token you can run this app yourself with the steps in the [github repository](https://github.com/gerardrbentley/streamlit-openai)

Made with ❤️ by [Gerard Bentley](https://gerardbentley.com)
"""
    )
    st.image("media/golang_demo.gif")

number_of_responses = st.sidebar.slider(
    "Number of Responses per Prompt Submission",
    1,
    10,
    1,
    1,
    help="A larger number may slow down response time",
)
temperature = st.sidebar.slider(
    "AI Temperature",
    0.0,
    1.0,
    1.0,
    0.1,
    help="A larger number means more random responses",
)
presence_penalty = st.sidebar.slider(
    "Presence Penalty",
    -2.0,
    2.0,
    0.0,
    0.1,
    help="A larger number means more new topics will come up",
)
frequency_penalty = st.sidebar.slider(
    "Frequency Penalty",
    -2.0,
    2.0,
    0.0,
    0.1,
    help="A larger number means fewer repeated phrases will come up",
)

with st.form("input"):
    chat_input = st.text_area("ChatGPT input:")
    is_submitted = st.form_submit_button()


request = ChatGPTRequest(
    messages=[
        ChatMessage("You are a helpful assistant", SYSTEM),
        ChatMessage(chat_input),
    ],
    n=number_of_responses,
    temperature=temperature,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty,
)

with st.expander("Sample Python Code"):
    formatted_kwargs = ',\n'.join((f'\t\t{key}={value!r}' for key, value in request.to_kwargs().items()))
    st.code(f"""\
import openai

openai.api_key = "load_your_api_key_string_here"
response = openai.ChatCompletion.create(
{formatted_kwargs}
)
chat_responses = response.get("choices")
""")

if not authenticated_user:
    st.stop()

if not is_submitted or not chat_input:
    st.warning("Enter text and hit Submit to continue!")
    st.stop()

try:
    with st.spinner("Generating response"):
        response = openai.ChatCompletion.create(**request.to_kwargs())
except Exception:
    logging.exception("Could not get ChatGPT response")
    st.error("Could not get response from ChatGPT API")
    st.stop()

with st.expander("Raw Response"):
    st.write(response)

chat_responses = response.get("choices")
if not chat_responses:
    st.warning("No 'choices' entry found in response")
    st.stop()

for i, chat_response in enumerate(chat_responses):
    st.header(f"Response {i + 1}:")
    st.write(chat_response.get("message", {}).get("content", "Unknown 'content'"))
