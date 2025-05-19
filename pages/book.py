import streamlit as st
from pageLinks import *
from dbms import get_book, get_author_by_book, check_borrowed, borrow_book_request, return_book
import datetime
from utils import *

bookid = st.session_state.bookid
book = get_book(bookid)
author = get_author_by_book(bookid)
st.session_state.pop("bookid", None)
user = st.session_state.user
userid = user['adminid'] if "adminid" in user else user['memberid']

borrowed = check_borrowed((userid, bookid)) if "memberid" in user else False

def borrow_or_return_book():
    st.session_state.bookid = bookid
    if borrowed:
        return_book(("returned", datetime.datetime.now(), bookid, userid))
    else:
        borrow_book_request(bookid, userid)
        alert(f"You have requested the book: \"{book['title']}\"")

def show_author():
    st.session_state.authorid = author['authorid']

if not book:
    st.header(str.title("Book not found!"))
else:
    col1, col2 = st.columns([1,2], gap='medium')

    with col1:
        st.markdown(f"""
            <img src="{book['image']}" style="aspect-ratio: 3 / 4; object-fit: cover;border-radius: 10px;"/>
        """, unsafe_allow_html=True)
    with col2:
        st.header(str.title(book['title']))
        st.text(book['publishedYear'])
        st.button(author['name'], type="tertiary", on_click=show_author)

        if "memberid" in user:
            if borrowed:
                currenttime = datetime.datetime.now()

                if currenttime > borrowed['duedate']:
                    st.error("Deadline: " + str(borrowed['duedate']))
                else:
                    st.warning("Deadline: " + str(borrowed['duedate']))
            st.button("Return" if borrowed else "Borrow", type="primary", on_click=borrow_or_return_book)
        else:
            st.text(f"Available Copies: {book['availableCopies']}")