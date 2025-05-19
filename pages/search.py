import streamlit as st
from pageLinks import *
from dbms import get_books
import html
from utils import *
from st_clickable_images import clickable_images

pg = st.navigation(
    [
        homePg,
        searchPg,
        logoutPg,
    ]
)

st.header(str.title("Search your favourite books here"))

if 'page' not in st.session_state:
    st.session_state.page = 1
if 'search_input' not in st.session_state:
    st.session_state.search_input = ""
if 'books' not in st.session_state:
    st.session_state.books = get_books(page=st.session_state.page)
if 'page_input' not in st.session_state:
    st.session_state.page_input = 1

def update_books():
    st.session_state.books = get_books(page=st.session_state.page, search=st.session_state.search_input)

def search():
    st.session_state.page = 1
    st.session_state.page_input = 1
    update_books()

def change_page():
    st.session_state.page = st.session_state.page_input
    update_books()

def prev_page():
    if st.session_state.page_input > 1:
        st.session_state.page_input -= 1
        st.session_state.page = st.session_state.page_input
        update_books()

def next_page():
    st.session_state.page_input += 1
    st.session_state.page = st.session_state.page_input
    update_books()

st.text_input(
    "Search",
    placeholder="Enter Book Name",
    key="search_input",
    label_visibility="collapsed",
    on_change=search
)

books = st.session_state.books

def print_hello():
    alert("Hello")

books = st.session_state.books

images = [book["image"] for book in books]
titles = [book["title"] for book in books]

st.session_state.clicked = clickable_images(
    images,
    titles=titles,
    div_style={"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "20px"},
    img_style={"width": "100%", "aspect-ratio": "3 / 4", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
)

if st.session_state.clicked != -1:
    book = books[st.session_state.clicked]
    if book:
        st.session_state.bookid = book['bookid']

col4, col5, col6 = st.columns(3)

with col5:
    sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])

    with sub_col1:
        st.button("", icon=":material/arrow_left:", use_container_width=True, on_click=prev_page, key="prev_btn")

    with sub_col2:
        st.number_input("", min_value=1, max_value=100, value=st.session_state.page_input, step=1,
                        label_visibility="collapsed", key="page_input_box", on_change=change_page)
        st.markdown("""
            <style>
            input[type=number] {
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

    with sub_col3:
        st.button("", icon=":material/arrow_right:", use_container_width=True, on_click=next_page, key="next_btn")
