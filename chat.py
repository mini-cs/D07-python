import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"

st.title("🤖 Gemini 챗봇")

if not API_KEY:
    st.error(".env에 GEMINI_API_KEY가 없어요. .env.example을 보고 채워 주세요")
    st.stop()

if "chat" not in st.session_state:
    # client를 따로 보관해야 함: 참조가 없으면 GC로 닫혀 RuntimeError(client has been closed)가 남
    st.session_state.client = genai.Client(api_key=API_KEY)
    st.session_state.chat = st.session_state.client.chats.create(model=MODEL)
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["text"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})
    try:
        answer = st.session_state.chat.send_message(prompt).text
    except Exception as e:
        # 예외 메시지에 요청 정보가 섞일 수 있어 종류만 출력
        answer = f"답변을 가져오지 못했습니다: {type(e).__name__}"
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "text": answer})
