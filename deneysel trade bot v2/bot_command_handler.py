import os
import time
import requests
import json

import config
from utils import get_balance
from position_manager import load_positions
from performance_analyzer import analyze_performance
from telegram_notifier import send_telegram_message

API_URL = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}"
OFFSET_FILE = "telegram_offset.txt"
PAUSE_FLAG = "paused.flag"


def _get_offset() -> int:
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r", encoding="utf-8") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def _save_offset(offset: int) -> None:
    with open(OFFSET_FILE, "w", encoding="utf-8") as f:
        f.write(str(offset))


def _handle_command(command: str) -> str:
    if command == "/status":
        balance = get_balance(config.BASE_CURRENCY)
        positions = load_positions()
        return f"Balance: {balance} {config.BASE_CURRENCY}\nPositions: {json.dumps(positions)}"
    if command == "/pnl":
        report = analyze_performance()
        return report or "No trade history"
    if command == "/pause":
        open(PAUSE_FLAG, "w").close()
        return "Bot paused"
    if command == "/resume":
        if os.path.exists(PAUSE_FLAG):
            os.remove(PAUSE_FLAG)
        return "Bot resumed"
    return "Unknown command"


def poll_commands(sleep_time: int = 5) -> None:
    """Continuously poll Telegram for new commands and respond."""
    offset = _get_offset()
    while True:
        try:
            resp = requests.get(f"{API_URL}/getUpdates", params={"timeout": 30, "offset": offset + 1})
            data = resp.json()
            if not data.get("ok"):
                time.sleep(sleep_time)
                continue
            for result in data.get("result", []):
                offset = result["update_id"]
                message = result.get("message", {})
                text = message.get("text", "")
                if text.startswith("/"):
                    reply = _handle_command(text.strip())
                    send_telegram_message(reply)
            _save_offset(offset)
        except Exception as exc:  # pragma: no cover - network issues
            print(f"Telegram polling error: {exc}")
        time.sleep(sleep_time)
