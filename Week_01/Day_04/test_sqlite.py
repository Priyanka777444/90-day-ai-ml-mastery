import sqlite3
from datetime import date, datetime

#connect to database (create file if doesn't exists)

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# creating a table
cursor.execute('''
      CREATE TABLE IF NOT EXISTs users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOL NULL,
               age INTEGER,
               created_at TEXT
    )
''')

#insert data
cursor.execute('''
    INSERT INTO users (name, age, created_at)
    VALUES (?,?,?)
''', ('Priyanka', 22, str(datetime.now())))

#save changes
conn.commit()

#read data
cursor.execute('SELECT*FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)

#close connection
conn.close