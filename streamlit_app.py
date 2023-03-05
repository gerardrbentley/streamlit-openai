import streamlit as st
import openai

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

with st.form("input"):
    chat_input = st.text_area("ChatGPT input:")
    is_submitted = st.form_submit_button()

if not is_submitted or not chat_input:
    st.warning("Enter text and hit Submit to continue!")
    st.stop()

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": chat_input}]
)

st.write(response)
