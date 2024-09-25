Advanced Keylogger with User Monitoring and Role-Based Blocking
Overview
This project demonstrates an Advanced Keylogger that monitors user activity, 
tracks keystrokes, clipboard activity, and monitors command usage in Command Prompt or PowerShell. 
It also includes role-based access control, allowing certain users to be blocked based on their actions, 
and logs are encrypted for secure storage. The second part of the project is a user-side script that checks if a user is blocked from login and performs actions accordingly.

Features
Keystroke Logging: Logs every keystroke, including special keys (space, enter, etc.).
Clipboard Monitoring: Detects and logs clipboard activity.
Command Monitoring: Detects specific commands (e.g., ipconfig, whoami) and triggers email alerts when these are used.
Role-Based Blocking: Blocks specific users based on the commands executed. Users are logged out of the system if detected.
Log Encryption: Keystroke logs are encrypted using Fernet encryption.
Email Alerts: Sends email alerts with encrypted logs and encryption keys when sensitive commands are detected.
GUI for Decryption and Unblocking: A graphical user interface (GUI) to decrypt log files and manage blocked users.
Project Structure
keylogger.py: Main keylogger file that tracks and logs user activity, encrypts logs, and handles email alerts.
block_user_script.py: Script that runs on the user's PC, checking if the user is blocked from logging in.
config.ini: Configuration file for email credentials.
encryption_key.key: File where the encryption key is stored for securing log files.
Setup Instructions
Clone the Repository:


git clone https://github.com/SecuritySphere/Advanced-Keylogger-with-User-Monitoring-and-Role-Based-Blocking.git
cd repository-name

Install Dependencies: Install required packages using pip:

pip install pynput cryptography pyperclip
Configure Email Settings:

Create a config.ini file and add your email credentials:
[Email]
sender_email = your-email@gmail.com
sender_password = your-email-password
Run the Keylogger:

To start the keylogger, execute the following command:

python keylogger.py
Run the Block User Script (User-Side):

Ensure the script runs on the user’s machine to check if they're blocked from login:
python block_user_script.py

Usage
Real-Time Monitoring: The keylogger will continuously monitor user activity in the background, logging keystrokes and clipboard content.
Role-Based Blocking: If a user executes certain commands (like whoami, ipconfig), they will be logged out based on their role (e.g., administrator, accounting).
Email Alerts: Upon detecting suspicious commands, the system sends email alerts with encrypted logs and the key to decrypt the log file.
GUI for Log Decryption and Unblocking Users
A graphical interface is provided to decrypt the encrypted log files and remove users from the blocked list.
Use this interface to manage blocked users and review the logs securely.
Future Enhancements
Remote Monitoring: Add functionality for remote monitoring of multiple users across systems.
Improved Role Management: Add more complex role-based actions and restrictions based on command usage and system activities.

Contributions
Feel free to contribute to the project by opening an issue or submitting a pull request.
