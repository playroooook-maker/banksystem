import sqlite3
from pathlib import Path
DB_PATH = Path("bank.db")
def _connect():
    return sqlite3.connect(DB_PATH)
def init():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        balance INTEGER NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account INTEGER,
        to_account INTEGER,
        amount INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
def save_account(account_id: int, balance: int):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO accounts (id, balance)
    VALUES (?, ?)
    ON CONFLICT(id) DO UPDATE SET balance = excluded.balance
    """, (account_id, balance))
    conn.commit()
    conn.close()
def save_transaction(from_id: int, to_id: int, amount: int):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (?, ?, ?)
    """, (from_id, to_id, amount))
    conn.commit()
    conn.close()
#int for c++