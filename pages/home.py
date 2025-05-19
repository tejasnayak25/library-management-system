import streamlit as st
from pageLinks import *
from dbms import get_borrow_requests, issue_book, get_borrowed_by_user, deny_book, get_logins_by_user, get_borrows_analytics_by_admin, get_borrows_analytics_by_user
from utils import *
import datetime
from st_clickable_images import clickable_images
import pandas as pd

pg = st.navigation([
    homePg,
    searchPg,
    logoutPg
])

cols = st.columns([5, 1], vertical_alignment="center")

with cols[0]:
    st.header(f"Welcome, {st.session_state.user['name']}")

with cols[1]:
    if st.button("Logout", icon=":material/logout:"):
        st.switch_page("pages/logout.py")

st.divider()

user = st.session_state.user
userid = user['adminid'] if "adminid" in user else user['memberid']
def update_books():
    st.session_state.borrow_requests = get_borrow_requests()

if "adminid" in user:
    if "borrow_requests" not in st.session_state:
        update_books()

    if "refresh_requests" not in st.session_state:
        st.session_state.refresh_requests = False

    if st.session_state.refresh_requests:
        update_books()
        st.session_state.refresh_requests = False

    st.subheader("Borrow Requests")
    if st.session_state.borrow_requests:
        for i, request in enumerate(st.session_state.borrow_requests):
            with st.container():
                cols = st.columns([1, 2, 2, 2, 1, 2])
                with cols[0]:
                    st.image(request["image"], width=60)
                with cols[1]:
                    st.markdown(f"**{request['title']}**")
                    st.caption(f"ISBN: {request['isbn']}")
                with cols[2]:
                    st.write("Published:")
                    st.write(f"{request['publishedYear']}")
                with cols[3]:
                    st.write("Member ID:")
                    st.write(f"{request['memberid']}")
                with cols[4]:
                    st.write("Copies:")
                    st.write(f"{request['availableCopies']}")
                with cols[5]:
                    if st.button("✅ Approve", key=f"approve_{i}"):
                        issuedate = datetime.datetime.now()
                        duedate = issuedate + datetime.timedelta(days=7)
                        issued = issue_book(("borrowed", issuedate, duedate, user['adminid'], request['bookid'], request['memberid']))
                        if(issued):
                            st.session_state.refresh_requests = True
                            st.rerun()
                        else:
                            alert("Failed to issue book!")
                    if st.button("❌ Deny", key=f"deny_{i}"):
                        deny_book(request['transactionid'])
                        st.session_state.refresh_requests = True
                        st.rerun()

        st.caption("Only pending requests are shown here.")
    else:
        st.info("No pending borrow requests.")
else:
    books = get_borrowed_by_user(userid)

    st.subheader("Borrowed Books")
    if(len(books) > 0):
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
    else:
        st.info("Nothing here!")

st.divider()

st.subheader("Your Activity")

option = st.radio("View by:", ["Day", "Month"], horizontal=True)

if option == "Day":
    period = "date"
else:
    period = "month"

data = get_logins_by_user(userid, period)
df = pd.DataFrame(data, columns=[period, "logins"])

st.bar_chart(df.set_index(period), x_label=period.title(), y_label="Logins")

if option == "Day":
    period = "date"
else:
    period = "month"

if "adminid" in user:
    st.subheader("Total Books Borrowed")
    data = get_borrows_analytics_by_admin(userid, period)
else:
    st.subheader("Borrowed Books")
    data = get_borrows_analytics_by_user(userid, period)

df = pd.DataFrame(data, columns=[period, "borrows"])

st.bar_chart(df.set_index(period), x_label=period.title(), y_label="Borrows")