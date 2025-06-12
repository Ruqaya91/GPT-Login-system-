import secrets
import time

# In-memory user store (username: password)
users = {
    "user1": "password123",
    "admin": "adminpass"
}

# In-memory token store (username: (token, expiry_time))
reset_tokens = {}

# Generate reset token
def generate_reset_token(username):
    if username not in users:
        print("User not found.")
        return

    token = secrets.token_urlsafe(16)
    expiry_time = time.time() + 300  # token valid for 5 minutes
    reset_tokens[username] = (token, expiry_time)
    
    print(f"Password reset token for {username}: {token} (valid for 5 minutes)")
    # In real system: send token by email/SMS

# Verify token and reset password
def reset_password(username, token, new_password):
    if username not in reset_tokens:
        print("No reset request found for this user.")
        return

    stored_token, expiry_time = reset_tokens[username]
    
    if time.time() > expiry_time:
        print("Token expired.")
        del reset_tokens[username]
        return

    if stored_token != token:
        print("Invalid token.")
        return

    users[username] = new_password
    del reset_tokens[username]
    print("Password successfully reset.")

# Simple interface
def main():
    while True:
        print("\n1. Login\n2. Request Password Reset\n3. Reset Password\n4. Exit")
        choice = input("Select option: ")

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            if username in users and users[username] == password:
                print("Login successful!")
            else:
                print("Invalid credentials.")

        elif choice == '2':
            username = input("Enter your username: ")
            generate_reset_token(username)

        elif choice == '3':
            username = input("Enter your username: ")
            token = input("Enter your reset token: ")
            new_password = input("Enter your new password: ")
            reset_password(username, token, new_password)

        elif choice == '4':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
