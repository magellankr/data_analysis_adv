import streamlit as st

st.header("🏠 Home")
st.write(f"Welcome, **{st.session_state.username}**!")

# 다른 페이지로 이동 (Streamlit 1.22+)
if st.button("분석 페이지로 가기"):
    st.switch_page("pages/2_📈_Analysis.py")
