import pandas
import uuid
import random
from dbms import add_authors, add_books

data = pandas.read_csv("books.csv", sep=";")
data = data.drop_duplicates(subset='ISBN', keep='first')

authors = []
aid={}

for author in data["Book-Author"].unique():
    if(not isinstance(author, str) or len(author) > 50):
        continue

    author_id = uuid.uuid4()

    year = random.randint(1900, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = f"{year}-{month:02d}-{day:02d}"

    email_name = author.strip().lower().replace(" ", ".")
    email = f"{email_name}@mail.com"
    aid[author] = str(author_id)

    authors.append((str(author_id), author, dob, email))

add_authors(authors)

books = []

for _, row in data.drop_duplicates(subset="ISBN").iterrows():
    author = row['Book-Author']
    if(not isinstance(author, str) or len(author) > 50):
        continue

    author_id = aid[author]
    book_id = uuid.uuid4()

    print(book_id)

    availableCopies = random.randint(1, 10)

    books.append((str(book_id), row['Book-Title'], row['ISBN'], int(row['Year-Of-Publication']), author_id, availableCopies, row['Image-URL-L']))

add_books(books)