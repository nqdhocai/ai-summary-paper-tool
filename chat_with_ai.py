import streamlit as st
from aicore import ChatSession

if "chatSession" not in st.session_state:
    st.session_state.chatSession = ChatSession()

st.title("💬 NQD's Chatbot")
st.caption("🚀 A Streamlit chatbot powered by NQDHOCAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "model", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = st.session_state.chatSession
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.get_response(prompt)
    msg = response
    st.session_state.messages.append({"role": "model", "content": msg})
    st.chat_message("assistant").write(msg)
