import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Demo", page_icon="🧭", layout="wide")

st.sidebar.success("왼쪽에서 페이지를 선택하세요.")

# 1) 로컬 MySQL 엔진 (한 번만 생성해서 재사용)
@st.cache_resource
def get_engine():
    # 로컬 설정에 맞게 수정
    USER = "root"
    PASSWORD = "0000"
    HOST = "127.0.0.1"   # 또는 "localhost"
    DB = "soloDB"

    url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}?charset=utf8mb4"
    # pre_ping: 연결 살아있는지 체크, pool_recycle: 오래된 커넥션 재생성
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800)

# 2) 쿼리 결과는 데이터 캐시 (engine을 인자로 받지 않음)
@st.cache_data(ttl=600)
def load_summary(sql: str):
    eng = get_engine()
    return pd.read_sql(sql, eng)

# (필요하면 세션 상태 초기화)
if "username" not in st.session_state:
    st.session_state.username = "guest"

# ── 테스트 출력 ──
st.title("MySQL 연결 테스트")
if st.button("요약 불러오기"):
    df = load_summary("SELECT CTY_RGN_NM, SUM(AMT) AS total_amt FROM company GROUP BY CTY_RGN_NM")
    st.dataframe(df, use_container_width=True)
