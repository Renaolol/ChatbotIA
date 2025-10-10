# streamlit_app.py
import streamlit as st
from agno.agent import RunEvent
from openai_agent import build_agent

@st.cache_resource(show_spinner="Inicializando agente...")
def get_agent():
    return build_agent()

agent = get_agent()

st.set_page_config(page_title="Chatbot IA", page_icon="🤖",layout="wide")
st.title("Chatbot com base na Resolução 5867-2020")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = agent.run(prompt)  # modo não-streaming
        answer = response.get_content_as_string()
        placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
