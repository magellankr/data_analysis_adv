import streamlit as st
import plotly.express as px
from app import get_engine, load_summary   # 공용 캐시 재사용

st.header("📈 Analysis")

df = load_summary("Select * from company")  # 캐시된 데이터 (페이지 전환해도 재사용)

st.dataframe(df, use_container_width=True)
fig = px.bar(df, x="CTY_RGN_NM", y="AMT", title="매출 요약")
st.plotly_chart(fig, use_container_width=True, key="sum_bar")
