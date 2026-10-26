
import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash


def get_user_details():
    username = input("Username: ").strip().lower()
    password = getpass("Choose a password: ")
    confirm_password = getpass("Confirm password: ")

    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    if password != confirm_password:
        raise ValueError("Passwords do not match.")

    return username, password


def save_user(action, username, password):
    password_hash = generate_password_hash(password)

    connection = sqlite3.connect("tasks.db")

    try:
        with connection:
            cursor = connection.cursor()

            if action == "create":
                cursor.execute(
                    """
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                    """,
                    (username, password_hash),
                )

            elif action == "reset":
                cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = ?
                    WHERE username = ?
                    """,
                    (password_hash, username),
                )

                if cursor.rowcount == 0:
                    raise ValueError("User not found.")

    finally:
        connection.close()


def main():
    print("1. Create user")
    print("2. Reset password")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        action = "create"
    elif choice == "2":
        action = "reset"
    else:
        print("Invalid option.")
        return

    try:
        username, password = get_user_details()
        save_user(action, username, password)

        if action == "create":
            print("User created successfully.")
        else:
            print("Password reset successfully.")

    except ValueError as error:
        print(f"Error: {error}")

    except sqlite3.IntegrityError:
        print("Could not create user. That username may already exist.")


if __name__ == "__main__":
    main()
