import logging

import streamlit as st
import openai

from interactors import ChatGPTRequest, ChatMessage, SYSTEM
from pocketbase import get_authenticated_user, PocketBaseUser

api_key = st.secrets.get("api_key")
if api_key is None:
    st.error("No api_key in .streamlit/secrets.toml")
    st.stop()
openai.api_key = api_key


def authenticate_pocketbase() -> PocketBaseUser:
    username = st.session_state.get("pocketbase_username")
    password = st.session_state.get("pocketbase_password")
    try:
        user = get_authenticated_user(username, password)
        st.session_state["user_key"] = user
    except Exception:
        logging.exception("Could not authenticate user")
        st.error("Error Logging In. Try again.")


def st_login() -> PocketBaseUser:
    authenticated_user: PocketBaseUser = st.session_state.get("user_key")
    if not authenticated_user:
        with st.form("sign_in", clear_on_submit=True):
            st.text_input(
                label="Username", 
                key="pocketbase_username",
            )
            st.text_input(
                label="Password", 
                key="pocketbase_password", 
                type="password",
            )
            st.form_submit_button("Log In", on_click=authenticate_pocketbase)
        st.warning("Not Logged In. Must Sign In to See Results")
    else:
        st.subheader(
            f"Welcome {authenticated_user.name or authenticated_user.username}!"
        )
    return authenticated_user
