import json
import os
from datetime import datetime, timedelta

POSITIONS_FILE = 'positions.json'

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_positions(positions):
    with open(POSITIONS_FILE, 'w') as f:
        json.dump(positions, f, indent=4)


def record_exit(symbol, timestamp=None):
    """Store the last exit time for a symbol."""
    positions = load_positions()
    if symbol not in positions:
        positions[symbol] = {}
    positions[symbol]['last_exit_time'] = (timestamp or datetime.now()).isoformat()
    save_positions(positions)


def can_reenter(symbol, cooldown_hours=1):
    """Return True if re-entry is allowed based on the last exit time."""
    positions = load_positions()
    info = positions.get(symbol)
    if not info or 'last_exit_time' not in info:
        return True
    last_exit = datetime.fromisoformat(info['last_exit_time'])
    return datetime.now() - last_exit > timedelta(hours=cooldown_hours)
