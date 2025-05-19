import streamlit as st
from utils import *
from pageLinks import *

st.set_page_config(initial_sidebar_state='collapsed')

if "logged_in" in st.session_state and st.session_state.logged_in:
    if "bookid" in st.session_state:
        pg = st.navigation([
            bookPg
        ])
    elif "authorid" in st.session_state:
        pg = st.navigation([
            authorPg
        ])
    else:
        pg = st.navigation([
            homePg, searchPg, logoutPg
        ])
else:
    pg = st.navigation([loginPg])

pg.run()