# Predefined users (username: password)
users = {
    "admin": "1234",
    "user1": "abcd",
    "guest": "guest"
}

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Run the login function
login()
