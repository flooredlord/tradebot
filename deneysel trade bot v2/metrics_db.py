import sqlite3
from contextlib import closing
from datetime import datetime

DB_PATH = "metrics.db"


def init_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS trades (symbol TEXT, side TEXT, price REAL, qty REAL, ts TEXT)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS pnl (symbol TEXT, pnl REAL, ts TEXT)"
        )
        conn.commit()


def log_trade(symbol: str, side: str, price: float, qty: float) -> None:
    ts = datetime.now().isoformat()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO trades (symbol, side, price, qty, ts) VALUES (?,?,?,?,?)",
            (symbol, side, price, qty, ts),
        )
        conn.commit()


def log_pnl(symbol: str, pnl: float) -> None:
    ts = datetime.now().isoformat()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO pnl (symbol, pnl, ts) VALUES (?,?,?)",
            (symbol, pnl, ts),
        )
        conn.commit()
