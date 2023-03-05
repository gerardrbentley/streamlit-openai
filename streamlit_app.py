import streamlit as st
import openai

from interactors import ChatGPTRequest, ChatMessage, SYSTEM

api_key = st.secrets.get("api_key")
if api_key is None:
    st.error("No api_key in .streamlit/secrets.toml")
    st.stop()
openai.api_key = api_key

user_keys = st.secrets.get("user_keys")
if user_keys is None or not isinstance(user_keys, list):
    st.error("No user_keys array in .streamlit/secrets.toml")
    st.stop()

query_params = st.experimental_get_query_params()
query_user_key_values = query_params.get("user_key")
if not query_user_key_values or not set(user_keys).intersection(query_user_key_values):
    st.error("Invalid User. Must be Admin with Key to continue")
    st.stop()

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

if not is_submitted or not chat_input:
    st.warning("Enter text and hit Submit to continue!")
    st.stop()

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

response = openai.ChatCompletion.create(**request.to_kwargs())

with st.expander("Raw Response"):
    st.write(response)

chat_responses = response.get("choices")
if not chat_responses:
    st.warning("No 'choices' entry found in response")
    st.stop()

for i, chat_response in enumerate(chat_responses):
    st.header(f"Response {i + 1}:")
    st.write(chat_response.get("message", {}).get("content", "Unknown 'content'"))
