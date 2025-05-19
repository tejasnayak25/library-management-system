import streamlit as st
from pageLinks import *
from dbms import get_author, get_books_by_author
from st_clickable_images import clickable_images

authorid = st.session_state.authorid
author = get_author(authorid)
books = get_books_by_author(authorid)
st.session_state.pop("authorid", None)

if not author:
    st.header(str.title("Author not found!"))
else:
    st.header(f"\"{str.title(author['name'])}\" Books:")
    
    images = [book["image"] for book in books]
    titles = [book["title"] for book in books]

    st.session_state.clicked = clickable_images(
        images,
        titles=titles,
        div_style={"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "20px"},
        img_style={"width": "100%", "aspect-ratio": "3 / 4", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
    )

    if st.session_state.clicked != -1:
        st.session_state.authorid = authorid
        book = books[st.session_state.clicked]
        if book:
            st.session_state.bookid = book['bookid']