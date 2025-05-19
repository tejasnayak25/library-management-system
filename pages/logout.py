import streamlit as st
from pageLinks import *
from dbms import save_login
import datetime

pg = st.navigation([
    homePg,
    searchPg
])

user = st.session_state.user

if not user:
    st.switch_page("pages/home.py")

if "adminid" in user:
    save_login((user['adminid'], "admin", st.session_state.logintime, datetime.datetime.now().time(), datetime.date.today()))
else:
    save_login((user['memberid'], "member", st.session_state.logintime, datetime.datetime.now().time(), datetime.date.today()))

st.session_state.clear()

st.switch_page("pages/home.py")