import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent / "bank.db"
# ПОДКЛЮЧЕНИЕ
def _connect():
    return sqlite3.connect(DB_PATH)
# ИНИЦИАЛИЗАЦИЯ БД
def init_db():
    conn = _connect()
    cur = conn.cursor()

    # Пользователи / счета
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        login TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
    """)
    # История переводов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER,
        to_id INTEGER,
        amount INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
# РЕГИСТРАЦИЯ
def create_user(login: str, password_hash: str) -> int | None:
    """
    Создаёт пользователя.
    Возвращает account_id или None если логин занят
    """
    account_id = hash(login) & 0x7FFFFFFF

    try:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO accounts (id, login, password_hash, balance)
        VALUES (?, ?, ?, 0)
        """, (account_id, login, password_hash))
        conn.commit()
        conn.close()
        return account_id
    except sqlite3.IntegrityError:
        return None
# ВХОД
def check_login(login: str, password_hash: str) -> int | None:
    """
    Проверка логина.
    Возвращает account_id или None
    """
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT id FROM accounts
    WHERE login=? AND password_hash=?
    """, (login, password_hash))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
# БАЛАНС
def get_balance(account_id: int) -> int | None:
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT balance FROM accounts WHERE id=?",
        (account_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def set_balance(account_id: int, new_balance: int) -> None:
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE accounts SET balance=? WHERE id=?",
        (new_balance, account_id)
    )
    conn.commit()
    conn.close()
# ПЕРЕВОД
def transfer(from_id: int, to_id: int, amount: int) -> int:
    """
    Возвращает:
    0  - успех
    -1 - неверная сумма
    -2 - счёт отправителя не найден
    -3 - счёт получателя не найден
    -4 - недостаточно средств
    """

    if amount <= 0:
        return -1

    from_balance = get_balance(from_id)
    to_balance = get_balance(to_id)

    if from_balance is None:
        return -2
    if to_balance is None:
        return -3
    if from_balance < amount:
        return -4

    set_balance(from_id, from_balance - amount)
    set_balance(to_id, to_balance + amount)

    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO transactions (from_id, to_id, amount)
    VALUES (?, ?, ?)
    """, (from_id, to_id, amount))
    conn.commit()
    conn.close()

    return 0
