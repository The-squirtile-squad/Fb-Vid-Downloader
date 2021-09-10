import pytest
import draft0
import sqlite3
from tkinter import messagebox


def tes(username, password):
    conn = sqlite3.connect('registrations.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM register")
    rec = c.fetchall()
    print(rec)

    db_username = [record[2] for record in rec]
    db_password = [record[3] for record in rec]

    if username in db_username and password in db_password:
        messagebox.showinfo("login", 'Correct username and password')
        return True
    else:
        messagebox.showinfo("Error", 'Invalid username and password')
        return False


assert tes('oopsie', '30090')
assert tes('Hi', '1234')
assert tes('', '')
assert tes('invalid_username', 'invalid_password')




