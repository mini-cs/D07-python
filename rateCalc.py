import json
import os
import urllib.error
import urllib.request

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGERATE_API_KEY")

CURRENCIES = {
    "KRW": ("🇰🇷 원", "#ff6b6b"),
    "USD": ("🇺🇸 달러", "#4ecdc4"),
    "EUR": ("🇪🇺 유로", "#a29bfe"),
    "JPY": ("🇯🇵 엔", "#fdcb6e"),
    "CNY": ("🇨🇳 위안", "#fd79a8"),
    "GBP": ("🇬🇧 파운드", "#74b9ff"),
}


@st.cache_data(ttl=3600)  # 환율은 1시간 단위로 갱신해도 충분
def fetch_rates(key, base):
    with urllib.request.urlopen(f"https://v6.exchangerate-api.com/v6/{key}/latest/{base}", timeout=10) as res:
        data = json.load(res)
    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "unknown"))
    return data["conversion_rates"]


st.title("💱 환율 계산기")

if not API_KEY:
    st.error(".env에 EXCHANGERATE_API_KEY가 없어요. .env.example을 보고 채워 주세요")
    st.stop()

col1, col2, col3 = st.columns(3)
amount = col1.number_input("금액", min_value=0.0, value=1000.0, step=100.0)
base = col2.selectbox("보내는 통화", list(CURRENCIES), format_func=lambda c: f"{c} {CURRENCIES[c][0]}")
targets = col3.multiselect(
    "받는 통화", [c for c in CURRENCIES if c != base], default=[c for c in CURRENCIES if c != base][:3],
    format_func=lambda c: f"{c} {CURRENCIES[c][0]}",
)

try:
    rates = fetch_rates(API_KEY, base)
except urllib.error.HTTPError as e:
    # 오류 메시지에 키가 담긴 URL이 나오지 않도록 상태 코드만 출력
    st.error(f"환율 정보를 가져오지 못했습니다: HTTP {e.code}")
    st.stop()
except Exception as e:
    st.error(f"환율 정보를 가져오지 못했습니다: {type(e).__name__} {e if isinstance(e, ValueError) else ''}")
    st.stop()

for cur in targets:
    name, color = CURRENCIES[cur]
    st.markdown(
        f"<div style='background:{color};color:white;padding:16px 20px;border-radius:12px;margin:8px 0'>"
        f"<div style='font-size:14px;opacity:.9'>{name} ({cur}) · 1 {base} = {rates[cur]:,.4f} {cur}</div>"
        f"<div style='font-size:28px;font-weight:bold'>{amount * rates[cur]:,.2f} {cur}</div></div>",
        unsafe_allow_html=True,
    )
