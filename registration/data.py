import sqlite3
from pathlib import Path

# Определяем путь к файлу базы данных.
# Path(__file__).parent говорит: "Ищи в той же папке, где лежит этот скрипт"
DB_PATH = Path(__file__).parent / "bank.db"


def _connect():
    """Служебная функция для открытия 'двери' в базу данных"""
    return sqlite3.connect(DB_PATH)


# --- ИНИЦИАЛИЗАЦИЯ (Создание структуры) ---
def init_db():
    """Создает таблицы (листы Excel), если их еще нет в файле bank.db"""
    conn = _connect()
    cur = conn.cursor()  # 'Библиотекарь', который будет выполнять запросы

    # Создаем таблицу пользователей (accounts)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,        -- Уникальный номер счета
        login TEXT UNIQUE NOT NULL,    -- Имя входа (не может повторяться)
        password_hash TEXT NOT NULL,   -- Зашифрованный пароль
        balance INTEGER NOT NULL       -- Сумма денег на счету
    )
    """)

    # Создаем таблицу истории переводов (transactions)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER,                -- ID того, кто отправил
        to_id INTEGER,                  -- ID того, кто получил
        amount INTEGER,                 -- Сколько денег
        created_at TEXT DEFAULT CURRENT_TIMESTAMP -- Время записи (ставится само)
    )
    """)

    conn.commit()  # Сохраняем изменения в файле
    conn.close()  # Закрываем дверь в базу


# --- ФУНКЦИИ ВХОДА И РЕГИСТРАЦИИ ---
def create_user(login: str, password_hash: str) -> int | None:
    """Регистрирует нового клиента"""
    # Генерируем ID на основе логина (как это делал твой друг)
    account_id = hash(login) & 0x7FFFFFFF
    try:
        conn = _connect()
        cur = conn.cursor()
        # Вопросительные знаки '?' — это защита от хакерских SQL-инъекций!
        cur.execute("""
        INSERT INTO accounts (id, login, password_hash, balance)
        VALUES (?, ?, ?, 1000)
        """, (account_id, login, password_hash))  # Вставляем данные вместо '?'
        conn.commit()
        conn.close()
        return account_id
    except sqlite3.IntegrityError:
        # Если такой логин уже есть в базе, SQLite выдаст ошибку IntegrityError
        return None


def check_login(login: str, password_hash: str) -> int | None:
    """Проверяет логин и пароль при входе"""
    conn = _connect()
    cur = conn.cursor()
    # Ищем строку, где совпали и логин, и пароль
    cur.execute("SELECT id FROM accounts WHERE login=? AND password_hash=?", (login, password_hash))
    row = cur.fetchone()  # Достаем одну найденную строку
    conn.close()
    return row[0] if row else None  # Если нашли — возвращаем ID, если нет — None


# --- ФУНКЦИИ ДЛЯ DASHBOARD (Личного кабинета) ---

def get_balance(account_id: int) -> int:
    """Просто узнает текущий баланс по ID"""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_transaction_history(user_id):
    """Достает историю переводов и красиво её оформляет (+/-)"""
    conn = _connect()
    cur = conn.cursor()

    # В этом большом запросе база сама решает:
    # 1. С кем был перевод (opponent)
    # 2. Какой знак поставить (|| склеивает текст и число)
    cur.execute("""
        SELECT 
            t.created_at, 
            CASE 
                WHEN t.from_id = ? THEN (SELECT login FROM accounts WHERE id = t.to_id)
                ELSE (SELECT login FROM accounts WHERE id = t.from_id) 
            END as opponent,
            CASE 
                WHEN t.from_id = ? THEN '-' || t.amount  -- Я отправил = Минус
                ELSE '+' || t.amount                  -- Мне прислали = Плюс
            END as display_amount
        FROM transactions t
        WHERE t.from_id = ? OR t.to_id = ?
        ORDER BY t.created_at DESC
    """, (user_id, user_id, user_id, user_id))

    history = cur.fetchall()  # Забираем все найденные строки истории
    conn.close()
    return history


def transfer_by_login(from_id, to_login, amount):
    """Главная логика перевода денег между пользователями"""

    # ПЕРВИЧНЫЕ ПРОВЕРКИ (Защита 'на берегу')
    if amount <= 0: return -1  # Нельзя отправить ноль или минус
    if amount > 10_000_000: return -6  # Твой лимит для защиты C++ типов

    conn = _connect()
    cur = conn.cursor()

    # 1. ПЕРЕВОДИМ ЛОГИН В ID (Находим получателя)
    cur.execute("SELECT id, balance FROM accounts WHERE login = ?", (to_login,))
    receiver = cur.fetchone()

    if not receiver:
        conn.close()
        return -3  # Ошибка: такого человека нет

    to_id = receiver[0]

    # 2. ПРОВЕРЯЕМ ДЕНЬГИ (Хватит ли у нас?)
    cur.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
    sender_balance = cur.fetchone()[0]

    if sender_balance < amount:
        conn.close()
        return -4  # Ошибка: недостаточно средств

    # 3. САМ ПЕРЕВОД (Транзакция)
    try:
        # Уменьшаем баланс у отправителя
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        # Увеличиваем баланс у получателя
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        # Записываем событие в историю
        cur.execute("INSERT INTO transactions (from_id, to_id, amount) VALUES (?, ?, ?)", (from_id, to_id, amount))

        conn.commit()  # Только здесь данные реально сохранятся в файл!
        res = 0  # Успех
    except Exception as e:
        print(f"Критическая ошибка базы: {e}")
        res = -5  # Что-то пошло не так на уровне SQL

    conn.close()
    return res