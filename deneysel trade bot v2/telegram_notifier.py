import requests
import config

def send_telegram_message(message):
    if not config.TELEGRAM_ENABLED:
        return

    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("Telegram credentials not set. Skipping notification.")
        return

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Telegram exception: {e}")