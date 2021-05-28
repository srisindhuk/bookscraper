import sqlite3
import requests
import pandas as pd
from pages.all_books_page import AllBooksPage
from main import books


def create_db_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS books(name text, price integer, rating integer)')
#    cursor.execute('CREATE TABLE IF NOT EXISTS books(name text, price integer, rating integer, description text)')

    connection.commit()
    connection.close()


def add_book(name, price, rating):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO books VALUES ("{name}", "{price}", "{rating}")')
#    cursor.execute(f'INSERT INTO books VALUES ("{name}", "{price}", "{rating}","{description})')

    connection.commit()
    connection.close()


def get_all_books():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books')
    allbooks = cursor.fetchall()
    print(len(allbooks))
    return allbooks



create_db_table()
for book in books:
#    add_book(book.name, book.price, book.rating, book.description)
    add_book(book.name, book.price, book.rating)


totalbooks = get_all_books()
data = pd.DataFrame(totalbooks, columns=["name", "price", "rating", "description"])
print(data)







