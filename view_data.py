import sqlite3

# Path to your SQLite database file
DB_PATH = 'employees.db'

def view_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute("SELECT * FROM employees")
    users = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    print("Columns:", column_names)
    print("\nUsers in the database:\n")
    for user in users:
        for col, val in zip(column_names, user):
            print(f"{col}: {val}")
        print("-" * 30)

    conn.close()

if __name__ == "__main__":
    view_users()
