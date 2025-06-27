import streamlit as st
import json
import os

USER_DATA_FILE = "users.json"


def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)


def signup(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists. Please login."
    users[username] = password
    save_users(users)
    return True, "Signup successful! Please login."


def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found. Please signup first."
    if users[username] != password:
        return False, "Incorrect password."
    return True, "Login successful!"


# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "rag_active" not in st.session_state:
    st.session_state.rag_active = False
if "crew_active" not in st.session_state:
    st.session_state.crew_active = False

# ------------------- UI -------------------

st.set_page_config(page_title="Login System", layout="centered")
st.title("Login / Signup Portal")

# Only show login/signup if not logged in
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error(message)

    with tab2:
        st.subheader("Signup")
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        if st.button("Signup"):
            success, message = signup(new_user, new_pass)
            if success:
                st.success(message)
            else:
                st.warning(message)

# ------------------- After Login -------------------

if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username}!")

    st.markdown("### Choose your assistant:")
    col1, col2 = st.columns(2)

    with col1:
        rag_clicked = st.button("RAG")
    with col2:
        crew_clicked = st.button("Crew")

    if rag_clicked:
        st.session_state.rag_active = True
        st.session_state.crew_active = False

    if crew_clicked:
        st.session_state.crew_active = True
        st.session_state.rag_active = False

    if st.session_state.rag_active:
        question = st.text_input("Ask a question to RAG Assistant:")
        if question:
            st.info(f"RAG processing: {question} (mock response)")

    if st.session_state.crew_active:
        question = st.text_input("Ask a question to Crew Assistant:")
        if question:
            st.info(f"Crew processing: {question} (mock response)")
