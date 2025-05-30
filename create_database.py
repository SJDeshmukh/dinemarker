import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop table if needed to recreate (uncomment if necessary)
cursor.execute('DROP TABLE IF EXISTS users')

# Updated users table schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        canteen_name TEXT,
        canteen_location TEXT,
        password TEXT NOT NULL
    )
""")

conn.commit()
conn.close()

print("Updated users table with new fields.")
