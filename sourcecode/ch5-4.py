import pandas as pd
import streamlit as st
# checkbox
#active = st.checkbox('I agree')

#if active:
#    st.text('Great!')
    
# checkbox on_change 인자 활용
def checkbox_write():
    if st.session_state.agree:   # key 이름 그대로 session_state에서 접근
        st.write("Great!")
    else:
        st.write("Unchecked!")

st.checkbox('I agree', key='agree', on_change=checkbox_write)

# toggle
toggle = st.toggle(
    'Turn on the switch!', value=True
)

if toggle:
    st.text('Switch is turned on!')
else:
    st.text('Switch is turned off!')

