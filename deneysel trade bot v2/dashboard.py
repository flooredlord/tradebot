import json
import os
import tkinter as tk
from tkinter import ttk


def load_history(path="trade_history.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def load_positions(path="positions.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def main():
    root = tk.Tk()
    root.title("TradeBot Dashboard")

    history = load_history()
    positions = load_positions()

    ttk.Label(root, text="Open Positions").pack(anchor="w")
    ttk.Label(root, text=json.dumps(positions, indent=2)).pack(anchor="w")

    ttk.Label(root, text="Trade History").pack(anchor="w")
    ttk.Label(root, text=json.dumps(history, indent=2)).pack(anchor="w")

    root.mainloop()


if __name__ == "__main__":
    main()
