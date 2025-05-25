import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    email TEXT UNIQUE,
    password TEXT
);
''')

# Commit and close
conn.commit()
conn.close()

print("Database and 'users' table created successfully.")
