import streamlit as st

st.header("🧰 Admin")
st.text_input("사용자명", key="username")   # 세션 상태 공유
st.write("현재 사용자:", st.session_state.username)
