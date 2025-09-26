import streamlit as st
from datetime import date, time

st.title("📊 Streamlit 입력 컨트롤 예제 🍖🍗 배고파")

# 문자열 입력
name = st.text_input("이름을 입력하세요", "")

# 숫자 입력
age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, value=20, step=1)

# 날짜 입력
birth_date = st.date_input("생년월일을 선택하세요", value=date(2000, 1, 1))

# 시간 입력
working_time = st.time_input("근무 시작 시간", value=time(9, 0))

# 카메라 입력
image = st.camera_input("사진을 찍어주세요")

# 결과 출력
st.subheader("입력 결과")
st.write(f"👤 이름: {name}")
st.write(f"🎂 나이: {age}")
st.write(f"📅 생년월일: {birth_date}")
st.write(f"⏰ 근무 시작 시간: {working_time}")

if image:
    st.image(image, caption="촬영한 이미지")
