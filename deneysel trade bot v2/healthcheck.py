import os
import time
import requests

CHECK_INTERVAL = 300
TARGET_URL = "https://api.binance.com/api/v3/time"


def is_alive() -> bool:
    try:
        requests.get(TARGET_URL, timeout=10)
        return True
    except Exception:
        return False


def monitor_and_restart(cmd: str) -> None:
    while True:
        if not is_alive():  # pragma: no cover - network
            print("Health check failed, restarting bot...")
            os.system(cmd)
        time.sleep(CHECK_INTERVAL)
