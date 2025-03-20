# bsb_family_pack2/core.py
import json
import os
from .telegram_utils import send_message

CONFIG_FILE = "bsb_config.json"

def connect_family(tg_token, tg_chat_id):
    config = {"tg_token": tg_token, "tg_chat_id": tg_chat_id}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    send_message(tg_token, tg_chat_id, "✅ A family member has connected to your Telegram integration!")
    print("Family connection established successfully.")

def disconnect_family():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        tg_token = config.get("tg_token")
        tg_chat_id = config.get("tg_chat_id")
        send_message(tg_token, tg_chat_id, "❌ Family connection has been disconnected!")
        os.remove(CONFIG_FILE)
        print("Family connection disconnected.")
    else:
        print("No active connection found.")
