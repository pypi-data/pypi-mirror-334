# bsb_family_pack2/telegram_utils.py
import requests

def send_message(tg_token, tg_chat_id, message):
    url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
    data = {"chat_id": tg_chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def send_document(tg_token, tg_chat_id, file_path):
    url = f"https://api.telegram.org/bot{tg_token}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": tg_chat_id}
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
    except Exception as e:
        print(f"Error sending document: {e}")
