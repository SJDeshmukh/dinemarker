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
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Drop the old table
c.execute('DROP TABLE IF EXISTS scans')

# Create correct table with employee_id
c.execute('''
    CREATE TABLE scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("✅ 'scans' table recreated successfully.")


