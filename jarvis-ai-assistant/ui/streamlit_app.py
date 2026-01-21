import streamlit as st
import requests
import uuid

API = "http://localhost:8000/chat"

st.title("🤖 Jarvis AI")

if "session" not in st.session_state:
    st.session_state.session = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        res = requests.post(API, json={
            "message": prompt,
            "session_id": st.session_state.session
        }).json()
        st.markdown(res["message"])
        st.session_state.messages.append(
            {"role": "assistant", "content": res["message"]}
        )
