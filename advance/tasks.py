import requests

from core.settings import TELEGRAM_BOT_TOKEN, GROUP_ID

def send_message_simple(user_id, text):

    for chat_id in [GROUP_ID, user_id]:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        if user_id == None:
            continue
        params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        requests.post(url, json=params)


def send_message_group(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": GROUP_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=params)