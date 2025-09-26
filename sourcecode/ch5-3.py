# button
import pandas as pd
import streamlit as st


def button_write():
    st.write('button activated')

#st.button('Reset', type='primary')
#st.button('activate', on_click=button_write) 

# 클릭 시 if문을 실행
if st.button('Reset', type='primary'):
    st.write('button reset')

if st.button('activate'):
    st.write('button activat')
    
