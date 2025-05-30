import sqlite3

# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()

# # Drop table if needed to recreate (uncomment if necessary)
# cursor.execute('DROP TABLE IF EXISTS users')

# # Updated users table schema
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         surname TEXT NOT NULL,
#         email TEXT NOT NULL UNIQUE,
#         phone TEXT,
#         canteen_name TEXT,
#         canteen_location TEXT,
#         password TEXT NOT NULL
#     )
# """)

# conn.commit()
# conn.close()

# print("Updated users table with new fields.")
# import sqlite3

# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# # Drop the old table
# c.execute('DROP TABLE IF EXISTS scans')

# c.execute('DROP TABLE IF EXISTS users')
# # Create correct table with employee_id
# c.execute('''
# CREATE TABLE scans (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     employee_id TEXT,
#     timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
#     raw_data TEXT
# );
# ''')

# conn.commit()
# conn.close()

# print("✅ 'scans' table recreated successfully.")

import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Drop existing tables (only for resetting)
c.execute('DROP TABLE IF EXISTS scans')
c.execute('DROP TABLE IF EXISTS users')

# Create users table with employee_id
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    canteen_name TEXT,
    canteen_location TEXT,
    password TEXT NOT NULL,
    employee_id TEXT UNIQUE NOT NULL
);
''')

# Create scans table
c.execute('''
CREATE TABLE scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);
''')

conn.commit()
conn.close()

print("✅ 'users' and 'scans' tables created successfully.")



