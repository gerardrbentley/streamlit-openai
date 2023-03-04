import streamlit as st

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.api_key = st.secrets["api_key"]

chat_input = st.text_area("ChatGPT input:")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": chat_input}]
)

st.write(response)
