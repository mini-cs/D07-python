import json
import os
import urllib.error
import urllib.parse
import urllib.request

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


@st.cache_data(ttl=600)  # 10분간 같은 결과 재사용 (API 호출 절약)
def fetch(key):
    query = urllib.parse.urlencode({"q": "Gimhae,KR", "appid": key, "units": "metric", "lang": "kr"})
    with urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?{query}", timeout=10) as res:
        return json.load(res)


st.title("김해 현재 날씨")

if not API_KEY:
    st.error(".env에 OPENWEATHER_API_KEY가 없어요. .env.example을 보고 채워 주세요")
    st.stop()

try:
    data = fetch(API_KEY)
except urllib.error.HTTPError as e:
    # 오류 메시지에 키가 담긴 URL이 나오지 않도록 상태 코드만 출력
    st.error(f"날씨 정보를 가져오지 못했습니다: HTTP {e.code}")
    st.stop()
except Exception as e:
    st.error(f"날씨 정보를 가져오지 못했습니다: {type(e).__name__}")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("기온", f"{data['main']['temp']}°C")
col2.metric("체감 온도", f"{data['main']['feels_like']}°C")
col3.metric("습도", f"{data['main']['humidity']}%")
st.subheader(f"날씨: {data['weather'][0]['description']}")
st.button("새로고침", on_click=st.cache_data.clear)
