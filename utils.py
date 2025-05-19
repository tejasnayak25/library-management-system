import streamlit as st

@st.dialog("Alert")
def alert(message):
    st.write(message)