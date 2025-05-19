import mysql
import mysql.connector
import os
lms = mysql.connector.connect(user='root', database='lms', password=os.environ['MYSQL_PASSWORD'])

def add_authors(author_list):
    cursor = lms.cursor()
    query = "INSERT INTO authors (authorid, name, dob, email) VALUES (%s, %s, %s, %s)"
    
    cursor.executemany(query, author_list)
    lms.commit()
    cursor.close()

def add_books(book_list):
    cursor = lms.cursor()
    query = "INSERT INTO books (bookid, title, isbn, publishedYear, authorid, availableCopies, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    cursor.executemany(query, book_list)
    lms.commit()
    cursor.close()

def save_login(data):
    cursor = lms.cursor()
    query = "INSERT INTO login (loginid, usertype, logintime, logouttime, date) VALUES (%s, %s, %s, %s, %s)"
    
    cursor.execute(query, data)
    lms.commit()
    cursor.close()

def borrow_book_request(bookid, memberid):
    cursor = lms.cursor()

    check_query = """
        SELECT transactionid FROM transactions
        WHERE bookid = %s AND memberid = %s AND (status = 'pending' OR status = 'borrowed')
    """
    cursor.execute(check_query, (bookid, memberid))
    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return False

    insert_query = """
        INSERT INTO transactions (bookid, memberid, status)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (bookid, memberid, 'pending'))
    lms.commit()
    cursor.close()
    return True

def issue_book(data):
    cursor = lms.cursor()

    bookid = data[4]

    cursor.execute("SELECT availableCopies FROM books WHERE bookid = %s", (bookid,))
    result = cursor.fetchone()

    if result is None or result[0] <= 0:
        cursor.close()
        return False

    query = """
        UPDATE transactions 
        SET status = %s, issuedate = %s, duedate = %s, issuedby = %s 
        WHERE bookid = %s AND memberid = %s
    """
    cursor.execute(query, data)

    cursor.execute("""
        UPDATE books 
        SET availableCopies = availableCopies - 1 
        WHERE bookid = %s
    """, (bookid,))

    lms.commit()
    cursor.close()
    return True

def deny_book(transactionid):
    cursor = lms.cursor()
    query = "DELETE from transactions WHERE transactionid = %s"
    
    cursor.execute(query, (transactionid, ))
    lms.commit()
    cursor.close()

def return_book(data):
    cursor = lms.cursor()
    
    status, returndate, bookid, memberid = data

    query = """
        UPDATE transactions 
        SET status = %s, returndate = %s 
        WHERE bookid = %s AND memberid = %s AND status = 'borrowed'
    """
    cursor.execute(query, (status, returndate, bookid, memberid))

    cursor.execute("""
        UPDATE books 
        SET availableCopies = availableCopies + 1 
        WHERE bookid = %s
    """, (bookid,))

    lms.commit()
    cursor.close()

def get_books(page=1, page_size=10, search=None):
    cursor = lms.cursor()

    offset = (page - 1) * page_size

    base_query = """
        SELECT bookid, title, isbn, publishedYear, authorid, availableCopies, image
        FROM books
    """

    params = []
    if search:
        base_query += " WHERE title LIKE %s"
        params.append(f"%{search}%")

    base_query += " ORDER BY publishedYear DESC LIMIT %s OFFSET %s"
    params.extend([page_size, offset])

    cursor.execute(base_query, params)

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books

def get_books_by_author(authorid):
    cursor = lms.cursor()

    base_query = """
        SELECT bookid, title, isbn, publishedYear, authorid, availableCopies, image
        FROM books 
        WHERE authorid = %s
    """

    cursor.execute(base_query, (authorid, ))

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books

def get_borrowed_by_user(userid):
    cursor = lms.cursor()

    base_query = """
        SELECT t.bookid, b.title, b.isbn, b.publishedYear, b.authorid, b.availableCopies, b.image,
               t.status, t.duedate
        FROM transactions t
        LEFT JOIN books b ON t.bookid = b.bookid
        INNER JOIN (
            SELECT bookid, MAX(duedate) AS max_due
            FROM transactions
            WHERE memberid = %s
            GROUP BY bookid
        ) latest ON latest.bookid = t.bookid AND latest.max_due = t.duedate
        WHERE t.memberid = %s
    """

    cursor.execute(base_query, (userid, userid))

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books

def get_borrow_requests():
    cursor = lms.cursor()

    base_query = """
        SELECT 
            t.transactionid,
            t.bookid, 
            b.title, 
            b.isbn, 
            b.publishedYear, 
            b.authorid, 
            b.availableCopies, 
            b.image,
            t.status, 
            t.duedate,
            t.memberid
        FROM transactions t
        LEFT JOIN books b ON t.bookid = b.bookid
        WHERE t.status = 'pending'
    """

    cursor.execute(base_query)

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books

def get_borrowed_by_user(userid):
    cursor = lms.cursor()

    base_query = """
        SELECT 
            t.bookid, 
            b.title, 
            b.isbn, 
            b.publishedYear, 
            b.authorid, 
            b.availableCopies, 
            b.image,
            t.status, 
            t.duedate,
            t.memberid
        FROM transactions t
        LEFT JOIN books b ON t.bookid = b.bookid
        WHERE t.status = 'borrowed' AND t.memberid = %s
    """

    cursor.execute(base_query, (userid, ))

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books

def check_borrowed(data):
    cursor = lms.cursor()

    query = """
        SELECT transactionid, duedate
        FROM transactions
        WHERE memberid = %s AND bookid = %s AND status = "borrowed"
    """

    cursor.execute(query, data)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()

    return dict(zip(columns, rows[0])) if rows else None

def get_book(id):
    cursor = lms.cursor()

    base_query = """
        SELECT bookid, title, isbn, publishedYear, authorid, availableCopies, image
        FROM books
        WHERE bookid=%s
    """

    cursor.execute(base_query, (id,))

    columns = [desc[0] for desc in cursor.description]
    books = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return books[0] if len(books) > 0 else None

def get_author_by_book(id):
    cursor = lms.cursor()

    base_query = """
        SELECT authorid, name, dob, email
        FROM authors
        WHERE authorid = (
            SELECT authorid FROM books WHERE bookid = %s
        )
    """

    cursor.execute(base_query, (id,))

    columns = [desc[0] for desc in cursor.description]
    authors = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return authors[0] if len(authors) > 0 else None

def get_author(id):
    cursor = lms.cursor()

    base_query = """
        SELECT authorid, name, dob, email
        FROM authors
        WHERE authorid = %s
    """

    cursor.execute(base_query, (id,))

    columns = [desc[0] for desc in cursor.description]
    authors = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return authors[0] if len(authors) > 0 else None

def get_user(user_type, email, password):
    cursor = lms.cursor()

    if user_type == "Admin":
        base_query = """
            SELECT adminid, name, email
            FROM admins
            WHERE email=%s and password=%s
        """
    else:
        base_query = """
            SELECT memberid, name, email, phone, address, datejoined
            FROM members
            WHERE email=%s and password=%s
        """

    cursor.execute(base_query, (email, password))

    columns = [desc[0] for desc in cursor.description]
    users = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return users[0] if len(users) > 0 else None

def get_logins_by_user(userid, period = "date"):
    cursor = lms.cursor()

    if period == "date":
        base_query = """
            SELECT DATE(date) as date, COUNT(*) as logins
            FROM login
            WHERE loginid = %s
            GROUP BY date
            ORDER BY date
        """
    else:
        base_query = """
            SELECT DATE_FORMAT(date, '%Y-%m') as month, COUNT(*) as logins
            FROM login
            WHERE loginid = %s
            GROUP BY month
            ORDER BY month
        """

    cursor.execute(base_query, (userid, ))

    columns = [desc[0] for desc in cursor.description]
    logins = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return logins

def get_borrows_analytics_by_admin(adminid, period = "date"):
    cursor = lms.cursor()

    if period == "date":
        base_query = """
            SELECT DATE(issuedate) as date, COUNT(*) as borrows
            FROM transactions
            WHERE issuedby = %s AND status = 'borrowed'
            GROUP BY date
            ORDER BY date
        """
    else:
        base_query = """
            SELECT DATE_FORMAT(issuedate, '%Y-%m') as month, COUNT(*) as borrows
            FROM transactions
            WHERE issuedby = %s AND status = 'borrowed'
            GROUP BY month
            ORDER BY month
        """

    cursor.execute(base_query, (adminid, ))

    columns = [desc[0] for desc in cursor.description]
    borrows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return borrows

def get_borrows_analytics_by_user(userid, period = "date"):
    cursor = lms.cursor()

    if period == "date":
        base_query = """
            SELECT DATE(issuedate) as date, COUNT(*) as borrows
            FROM transactions
            WHERE memberid = %s AND status = 'borrowed'
            GROUP BY date
            ORDER BY date
        """
    else:
        base_query = """
            SELECT DATE_FORMAT(issuedate, '%Y-%m') as month, COUNT(*) as borrows
            FROM transactions
            WHERE memberid = %s AND status = 'borrowed'
            GROUP BY month
            ORDER BY month
        """

    cursor.execute(base_query, (userid, ))

    columns = [desc[0] for desc in cursor.description]
    borrows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    return borrows