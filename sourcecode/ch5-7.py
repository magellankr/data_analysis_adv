import pandas as pd
import streamlit as st
# text input
string = st.text_input(
    'Movie title', placeholder='write down the title of your favorite movie', key="1"
)

if string:
    st.text('Your answer is '+string)
    
# password 인자 활용
string = st.text_input(
    'Movie title',
    placeholder='write down the title of your favorite movie',
    type='password', key="2"
)

if string:
    st.text('Your answer is '+string)