import sqlite3


def get_all_books() -> list:
    try:
        with sqlite3.connect("data_base/users_account.db") as con:
            cur = con.cursor()
            books = cur.execute("SELECT id_book, name, author, description, price, photo FROM books").fetchall()
        return books
    except Exception as e:
        print(e)


def search_for_book_in_bd(name: str, author: str) -> tuple:
    try:
        with sqlite3.connect("data_base/users_account.db") as con:
            cur = con.cursor()
            book = cur.execute("SELECT name, author, description, price, photo FROM books WHERE name=? AND author=?",
                               (name, author)).fetchone()
        return book
    except Exception as e:
        print(e)


def add_new_book(name: str, author: str, description: str, price: int, photo: str):
    try:
        with sqlite3.connect("data_base/users_account.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                        (name, author, description, price, photo))
    except Exception as e:
        print(e)


def delete_book(id_book: int):
    try:
        with sqlite3.connect("data_base/users_account.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM books WHERE id = ?", (id_book,))
    except Exception as e:
        print(e)
