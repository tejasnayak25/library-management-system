Library Management System (Streamlit)
=====================================

Interactive Streamlit app backed by MySQL that lets admins approve/deny borrow requests and members browse, borrow, and return books. The UI uses Streamlit's multi-page navigation to keep flows simple while persisting session state.

Features
--------
- Member experience: browse/search books with pagination and cover previews, open details, submit borrow requests, and return borrowed items.
- Admin experience: review pending borrow requests, approve or deny, and view borrowing/login analytics.
- Auth: simple email/password login for admin or member roles (sample users seeded in SQL).
- Data: MySQL schema for authors, books, members, admins, transactions, and login activity with optional seeding from `books.csv`.

Stack
-----
- Streamlit app entrypoint: [app.py](app.py)
- Page routing definitions: [pageLinks.py](pageLinks.py)
- Pages: [pages/home.py](pages/home.py), [pages/search.py](pages/search.py), [pages/book.py](pages/book.py), [pages/author.py](pages/author.py), [pages/login.py](pages/login.py), [pages/logout.py](pages/logout.py)
- DB access layer: [dbms.py](dbms.py)
- Utilities (alert dialog): [utils.py](utils.py)
- Sample data + seeder: [books.csv](books.csv), [trial2.py](trial2.py)
- Schema reference: [db.sql](db.sql)

Prerequisites
-------------
- Python 3.10+ (tested with Streamlit navigation APIs introduced in Streamlit 1.40+).
- MySQL server running locally with a user that can create the `lms` database.
- Set environment variable `MYSQL_PASSWORD` to the MySQL user password before running the app.

Setup
-----
1) Clone and enter the repo
```
git clone https://github.com/tejasnayak25/library-management-system.git
cd library-management-system
```

2) Create and activate a virtual environment (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\activate
```

3) Install dependencies
```
pip install streamlit mysql-connector-python pandas st-clickable-images
```

4) Configure the database
- Ensure `MYSQL_PASSWORD` is set in your shell.
- Start MySQL and execute the schema script:
```
mysql -u root -p < db.sql
```

5) (Optional) Seed sample book and author data
```
python trial2.py
```
This reads `books.csv` and populates `authors` and `books` via `add_authors` and `add_books` in [dbms.py](dbms.py).

6) Run the app
```
streamlit run app.py
```

Login Accounts (from db.sql)
-----------------------------
- Admin: email `tejas@xyz.com`, password `abcde`
- Member: email `syesh@xyz.com`, password `12345`

How It Works
------------
- Navigation: [app.py](app.py) chooses the page set based on `st.session_state.logged_in`, `bookid`, and `authorid`. Pages are registered in [pageLinks.py](pageLinks.py).
- Book search: [pages/search.py](pages/search.py) fetches paginated results from `get_books` with optional title search and uses clickable cover images to set `st.session_state.bookid`.
- Book detail: [pages/book.py](pages/book.py) shows metadata, lets members request or return a book, and routes to author details.
- Author detail: [pages/author.py](pages/author.py) lists books by that author.
- Home/dashboard: [pages/home.py](pages/home.py) shows borrow requests for admins (approve/deny/issue) or borrowed books and activity charts for members/admins.
- Auth and session: [pages/login.py](pages/login.py) sets `st.session_state.user`, `logged_in`, and login time; [pages/logout.py](pages/logout.py) records login activity and clears the session.
- Data layer: [dbms.py](dbms.py) wraps MySQL queries for books, authors, users, transactions, and analytics; it expects `MYSQL_PASSWORD` in the environment.

Troubleshooting
---------------
- MySQL auth errors: verify `MYSQL_PASSWORD` is set and the MySQL user has privileges to create/use the `lms` database.
- Streamlit cannot import `st.navigation` or `st.Page`: upgrade Streamlit to >= 1.40.
- No books appear: confirm `books` table is populated (run `python trial2.py` after executing `db.sql`).

Notes
-----
- This project uses a simple, inline password scheme for demo purposes; do not use in production without proper auth and hashing.
- Images are referenced via URLs stored in the `image` column; ensure outbound network access if running in restricted environments.
