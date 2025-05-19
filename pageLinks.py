import streamlit as st

homePg = st.Page("./pages/home.py", title="Home", url_path="/")
loginPg = st.Page("./pages/login.py", title="Login", url_path="/login")
searchPg = st.Page("./pages/search.py", title="Search", url_path="/search")
logoutPg = st.Page("./pages/logout.py", title="Logout", url_path="/logout")
bookPg = st.Page("./pages/book.py", title="Book Details", url_path="/book")
authorPg = st.Page("./pages/author.py", title="Author Details", url_path="/author")