import streamlit as st
import requests
import json

FASTAPI_URL = "http://localhost:8080/chat/"

st.set_page_config(page_title="MCP Agent")
st.title("MCP Agent")

if "messages" not in st.session_state:
    st.session_state["messages"]= [{"role": "ai", "content": "Hello! How can i help you tody"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        FASTAPI_URL, 
        json={"message": prompt}
    )

    response_data = response.json()
    print(response_data)
    ai_response = response_data["response"]

    st.session_state.messages.append({"role": "ai", "content": ai_response})

    with st.chat_message("ai"):
        st.markdown(ai_response)

    st.rerun()