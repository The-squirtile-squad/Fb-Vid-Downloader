import sqlite3

conn = sqlite3.connect('registrations.db')
print(conn.cursor().fetchall())