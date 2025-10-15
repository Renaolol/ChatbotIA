import os
from typing import Dict

import streamlit as st
from dotenv import load_dotenv

from openai_agent import build_agent


@st.cache_resource(show_spinner="Inicializando agente...")
def get_agent():
    return build_agent()


def _parse_credentials(raw: str) -> Dict[str, str]:
    credentials: Dict[str, str] = {}
    if not raw:
        return credentials

    entries = [entry.strip() for entry in raw.split(";") if entry.strip()]
    for entry in entries:
        if ":" not in entry:
            continue
        username, password = entry.split(":", 1)
        credentials[username.strip()] = password.strip()
    return credentials


def require_authentication(credentials: Dict[str, str]) -> None:
    if not credentials:
        st.error("Nenhum usuário configurado. Defina APP_USERS no .env (ex.: usuario:senha;admin:1234).")
        st.stop()

    if "auth_status" not in st.session_state:
        st.session_state.auth_status = False
        st.session_state.auth_user = None

    if st.session_state.auth_status:
        return

    st.title("Chatbot com base na Resolução 5867-2020")
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if credentials.get(username) == password:
                st.session_state.auth_status = True
                st.session_state.auth_user = username
                st.success("Login realizado com sucesso.")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
    st.stop()


def maybe_logout() -> None:
    if st.sidebar.button("Sair"):
        st.session_state.auth_status = False
        st.session_state.auth_user = None
        st.session_state.messages = []
        st.rerun()


load_dotenv()
USER_CREDENTIALS = _parse_credentials(os.getenv("APP_USERS", ""))

st.set_page_config(page_title="Chatbot IA", page_icon="🤖", layout="wide")

require_authentication(USER_CREDENTIALS)

st.title("Chatbot com base na Resolução 5867-2020")
st.caption(f"Usuário autenticado: {st.session_state.auth_user}")
maybe_logout()

agent = get_agent()

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
