import hashlib
import getpass  # For hiding password input

# Hashed password for demonstration (replace with your actual hashed password)
stored_hash = "b6ed35e82cc571aa70dde3d57da6c7ed4cdd122be520c32c56c76fdb5566715d"          #asus pd-"5d11339ba565bff5d4b2137a28fe440999af3f54980c36e6c6b76f012c28f6c5"

# Function to authenticate admin
def authenticate_admin():
    while True:
        password = getpass.getpass("Enter admin password: ")
        hashed_input = hashlib.sha256(password.encode()).hexdigest()

        if hashed_input == stored_hash:
            return True
        else:
            print("Authentication failed. Invalid password.")
            choice = input("Enter 'q' to quit or any other key to try again: ")
            if choice.lower() == 'q':
                return False

# Function to display main menu
def display_menu():
    print("\nAdmin Menu:")
    print("1. View Blocked Users")
    print("2. Unblock User")
    print("3. Exit")

# Function to view blocked users
def view_blocked_users():
    try:
        with open("C:/ProgramData/blocked_user.txt", "r") as f:
            blocked_users = f.readlines()
        if blocked_users:
            print("\nList of Blocked Users:")
            for user in blocked_users:
                print(user.strip())
        else:
            print("No users are currently blocked.")
    except FileNotFoundError:
        print("No blocked users.")

# Function to unblock user
def unblock_user():
    try:
        with open("C:/ProgramData/blocked_user.txt", "r") as f:
            blocked_users = f.readlines()
        
        username = input("Enter username to unblock: ").strip()  # Strip whitespace from input

        if username + "\n" in blocked_users:
            blocked_users.remove(username + "\n")
            with open("C:/ProgramData/blocked_user.txt", "w") as f:
                f.writelines(blocked_users)
            print(f"User {username} has been unblocked.")
        else:
            print(f"User {username} is not blocked.")
    except FileNotFoundError:
        print("No blocked users.")

# Main function
def main():
    authenticated = authenticate_admin()
    if not authenticated:
        print("Authentication failed. Exiting program.")
        return
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            view_blocked_users()
        elif choice == "2":
            unblock_user()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
