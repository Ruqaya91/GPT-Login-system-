import sqlite3
import hashlib

# Connect to SQLite database (creates the file if not exists)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register function
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try another.")

# Login function
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    result = cursor.fetchone()
    if result:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Main program
def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select option: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid option. Try again.")

# Run the program
if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
