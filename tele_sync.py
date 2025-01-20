import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askdirectory
from datetime import datetime
import uuid
import json

root = Tk()
root.withdraw()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DEFAULT_FOLDER = "C:/Users/user/Desktop"
CONFIG_FILE = "upload_config.json"

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN and CHAT_ID must be set in .env file")

def load_saved_folder():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('folder_path', DEFAULT_FOLDER)
    except FileNotFoundError:
        return DEFAULT_FOLDER

def save_folder_path(folder_path):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'folder_path': folder_path}, f)

def generate_timestamp(original_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    unq_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unq_id}{ext}"

def upload_files():
    folder_path = load_saved_folder()
    
    if not os.path.exists(folder_path):
        print("Saved folder not found. Please select a new folder.")
        folder_path = askdirectory()
        if not folder_path:  # If user cancels selection
            print("No folder selected. Exiting...")
            return
        save_folder_path(folder_path)
    
    print(f"Using folder: {folder_path}")

    # First, count total files
    total_files = sum([len(files) for _, _, files in os.walk(folder_path)])
    
    with requests.Session() as s:
        # Create progress bar
        with tqdm(total=total_files, desc="Uploading files") as pbar:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    unique_filename = generate_timestamp(file)
                    try:
                        with open(file_path, "rb") as f:
                            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                            files = {
                                "document": (unique_filename, f, "application/octet-stream")
                            }
                            response = s.post(url, 
                                           data={"chat_id": CHAT_ID}, 
                                           files=files)
                            if response.status_code != 200:
                                print(f"\nFailed to upload {file_path}")
                            else:
                                pbar.set_postfix_str(f"Current file: {unique_filename}")
                            pbar.update(1)
                    except Exception as e:
                        print(f"\nError uploading {file_path}: {str(e)}")

if __name__ == "__main__":
    upload_files()