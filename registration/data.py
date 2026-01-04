import sqlite3
from pathlib import Path

DB_PATH = Path("bank.db")


def _connect():
    return sqlite3.connect(DB_PATH)


def init():
    conn = _connect()
    cur = conn.cursor()

    # АККАУНТЫ
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        login TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
    """)

    # ТРАНЗАКЦИИ
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


def create_user(account_id: int, login: str, password_hash: str, balance: int = 0):
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO accounts (id, login, password_hash, balance)
    VALUES (?, ?, ?, ?)
    """, (account_id, login, password_hash, balance))

    conn.commit()
    conn.close()


def check_user_login(login: str, password_hash: str):
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, balance FROM accounts
    WHERE login = ? AND password_hash = ?
    """, (login, password_hash))

    result = cur.fetchone()
    conn.close()
    return result


def save_transaction(from_id: int, to_id: int, amount: int):
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (?, ?, ?)
    """, (from_id, to_id, amount))

    conn.commit()
    conn.close()
