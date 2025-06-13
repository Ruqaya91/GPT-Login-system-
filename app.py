import secrets
import datetime

# --- Mock Database ---
# In a real application, this would be a database (SQL, NoSQL, etc.)
# We're using simple dictionaries to simulate user data and token storage.

# Stores user information (username, password hash in a real app)
users_db = {
    "user1@example.com": {"username": "user1", "password_hash": "hashed_password_for_user1"},
    "user2@example.com": {"username": "user2", "password_hash": "hashed_password_for_user2"},
}

# Stores active password reset tokens
# Key: email, Value: {"token": "generated_token", "expiry_time": datetime_object}
password_reset_tokens_db = {}


# --- Password Reset Functions ---

def generate_reset_token(email: str, expiry_minutes: int = 60) -> str | None:
    """
    Generates a secure, random token for password reset and stores it with an expiry time.

    Args:
        email (str): The email address of the user requesting a reset.
        expiry_minutes (int): The number of minutes until the token expires.

    Returns:
        str | None: The generated token if the email exists, otherwise None.
    """
    if email not in users_db:
        print(f"Error: User with email '{email}' not found.")
        return None

    # Generate a URL-safe text string, suitable for use in URLs.
    # A length of 32 bytes (256 bits) is generally considered secure for tokens.
    token = secrets.token_urlsafe(32)

    # Calculate expiry time
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)

    # Store the token with its expiry time
    password_reset_tokens_db[email] = {
        "token": token,
        "expiry_time": expiry_time
    }
    print(f"Generated reset token for {email}: {token}. Expires at {expiry_time}")
    return token

def validate_reset_token(email: str, token: str) -> bool:
    """
    Validates a given password reset token for a specific email.

    Args:
        email (str): The email address associated with the token.
        token (str): The token to validate.

    Returns:
        bool: True if the token is valid and not expired, False otherwise.
    """
    if email not in password_reset_tokens_db:
        print(f"Validation failed: No token found for {email}.")
        return False

    stored_token_info = password_reset_tokens_db[email]
    stored_token = stored_token_info["token"]
    expiry_time = stored_token_info["expiry_time"]

    if token != stored_token:
        print(f"Validation failed: Mismatch token for {email}.")
        return False

    if datetime.datetime.now() > expiry_time:
        print(f"Validation failed: Token for {email} has expired.")
        # Optionally, remove expired token from DB
        del password_reset_tokens_db[email]
        return False

    print(f"Validation successful: Token for {email} is valid.")
    return True

def reset_password(email: str, token: str, new_password: str) -> bool:
    """
    Resets the user's password after successful token validation.

    Args:
        email (str): The user's email.
        token (str): The reset token provided by the user.
        new_password (str): The new password to set.

    Returns:
        bool: True if the password was reset, False otherwise.
    """
    if validate_reset_token(email, token):
        # In a real application, you would hash new_password here
        # and update the 'password_hash' in the users_db.
        users_db[email]["password_hash"] = f"new_hashed_password_for_{email}"
        print(f"Password for {email} has been successfully reset.")
        # Invalidate the token after successful use
        if email in password_reset_tokens_db:
            del password_reset_tokens_db[email]
            print(f"Reset token for {email} has been invalidated.")
        return True
    else:
        print(f"Password reset failed for {email} due to invalid or expired token.")
        return False

# --- Example Usage ---
if __name__ == "__main__":
    user_email_1 = "user1@example.com"
    user_email_2 = "user2@example.com"
    non_existent_email = "nonexistent@example.com"

    print("--- Scenario 1: Successful Password Reset ---")
    # User 1 requests a password reset
    token1 = generate_reset_token(user_email_1, expiry_minutes=1) # Token expires in 1 minute

    if token1:
        # Simulate a delay (e.g., user checking email, clicking link)
        import time
        # time.sleep(5) # Uncomment to test token expiration

        # User 1 attempts to reset password with the token
        print(f"\nAttempting to reset password for {user_email_1} with token: {token1}")
        reset_success = reset_password(user_email_1, token1, "MyNewSecurePassword123!")

        if reset_success:
            print(f"Current password hash for {user_email_1}: {users_db[user_email_1]['password_hash']}")
        else:
            print(f"Password reset for {user_email_1} failed.")

    print("\n--- Scenario 2: Invalid Token Attempt ---")
    token2_invalid = generate_reset_token(user_email_2) # Generate a token for user 2
    if token2_invalid:
        print(f"\nAttempting to reset password for {user_email_2} with an INVALID token.")
        reset_password(user_email_2, "AN_INCORRECT_TOKEN", "AnotherNewPassword!")

    print("\n--- Scenario 3: Expired Token Attempt (uncomment time.sleep to see effect) ---")
    # To test expiration, uncomment the time.sleep(5) line above and set expiry_minutes to a small value (e.g., 1)
    # The token for user1 in Scenario 1 would likely be expired if sleep is enabled.
    print(f"Re-attempting reset for {user_email_1} with potentially expired token {token1} (if scenario 1 had sleep enabled).")
    if token1: # Assuming token1 was generated successfully earlier
        reset_password(user_email_1, token1, "YetAnotherPassword!")

    print("\n--- Scenario 4: Non-existent User Request ---")
    generate_reset_token(non_existent_email)

    print("\n--- Current State of Password Reset Tokens DB ---")
    print(password_reset_tokens_db)

