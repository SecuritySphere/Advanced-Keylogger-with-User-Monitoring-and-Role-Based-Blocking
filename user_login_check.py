import os

blocked_users_file = r'Path/to/blocked_user.txt'
username = os.getenv('USERNAME')

if os.path.exists(blocked_users_file):
    with open(blocked_users_file, 'r') as file:
        blocked_users = file.read().splitlines()
        if username in blocked_users:
            print(f"Access denied for {username}")
            os.system("shutdown -l")  # Exit with an error code to prevent login
