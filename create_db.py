import sqlite3

conn = sqlite3.connect('news.db')
conn.execute('CREATE TABLE IF NOT EXISTS newsletter (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
conn.close()
print("Database created.")
