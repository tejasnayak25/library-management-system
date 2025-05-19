import streamlit as st
import json
from utils import *
from dbms import get_user
import datetime

def login():
    user = get_user(st.session_state.login_type, st.session_state.email, st.session_state.password)
    if(user):
        alert("Logged in successfully!")
        st.session_state.logged_in = True
        st.session_state.user = user
        st.session_state.logintime = datetime.datetime.now().time()
    else:
        alert("Login failed!")


col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.header("Login", anchor=None)
    st.selectbox("Login as", ("User", "Admin"), key="login_type")
    st.text_input("Email", placeholder="Enter email", key="email")
    st.text_input("Password", placeholder="Enter password", key="password")
    st.button("Login", icon=":material/login:", type="primary", on_click=login)

with col3:
    st.write(' ')