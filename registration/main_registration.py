import tkinter as tk
from tkinter import messagebox
import hashlib # Для шифрования паролей
import data # Наша база данных
from dashboard import DashboardApp # Класс дашборда, который откроется после входа

# При запуске файла создаем таблицы в базе, если их еще нет
data.init_db()

# --- УТИЛИТЫ ДЛЯ БЕЗОПАСНОСТИ ---

def check_safety(text: str) -> bool:
    """Проверка текста на опасные символы (защита от взлома SQL)"""
    forbidden = "/^:;\"'--*"
    # Проверяем, есть ли хотя бы один плохой символ в тексте
    return not any(c in forbidden for c in text)

def get_hash(password: str) -> str:
    """Превращает обычный пароль в длинный непонятный код (хеш)"""
    # Пароль нельзя хранить в чистом виде, только в виде хеша
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# --- ОКНО ВХОДА ---

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank | Вход")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        # Отрисовка полей логина и пароля
        tk.Label(root, text="Логин", font=("Arial", 14)).pack(pady=10)
        self.entry_login = tk.Entry(root, font=("Arial", 14))
        self.entry_login.pack()

        tk.Label(root, text="Пароль", font=("Arial", 14)).pack(pady=10)
        # show="*" скрывает вводимые символы пароля
        self.entry_password = tk.Entry(root, show="*", font=("Arial", 14))
        self.entry_password.pack()

        # Кнопка входа
        tk.Button(
            root, text="Войти", font=("Arial", 14),
            bg="#2ecc71", fg="white", command=self.login
        ).pack(pady=15)

        # Кнопка перехода к регистрации
        tk.Button(
            root, text="Создать аккаунт", font=("Arial", 12),
            command=self.open_register
        ).pack()

    def login(self):
        """Проверка данных и вход в систему"""
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()

        # Проверка на пустые поля
        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        # Проверка на безопасность (чтобы не взломали SQL)
        if not check_safety(login) or not check_safety(password):
            messagebox.showerror("Ошибка", "Запрещённые символы")
            return

        # Получаем хеш введенного пароля и идем в базу проверять
        password_hash = get_hash(password)
        user_id = data.check_login(login, password_hash)

        if user_id is None:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            return

        # Если данные верны: закрываем окно входа и открываем Дашборд
        self.root.destroy()
        DashboardApp(user_id)

    def open_register(self):
        """Открывает окно регистрации поверх текущего"""
        RegisterWindow(self.root)

# --- ОКНО РЕГИСТРАЦИИ ---

class RegisterWindow:
    def __init__(self, master):
        # Toplevel создает новое окно поверх главного
        self.window = tk.Toplevel(master)
        self.window.title("Регистрация")
        self.window.geometry("420x320")
        self.window.resizable(False, False)

        # Поля для логина и двух паролей (для проверки на опечатку)
        tk.Label(self.window, text="Логин", font=("Arial", 14)).pack(pady=10)
        self.entry_login = tk.Entry(self.window, font=("Arial", 14))
        self.entry_login.pack()

        tk.Label(self.window, text="Пароль", font=("Arial", 14)).pack(pady=10)
        self.entry_password1 = tk.Entry(self.window, show="*", font=("Arial", 14))
        self.entry_password1.pack()

        tk.Label(self.window, text="Повтор пароля", font=("Arial", 14)).pack(pady=10)
        self.entry_password2 = tk.Entry(self.window, show="*", font=("Arial", 14))
        self.entry_password2.pack()

        tk.Button(
            self.window, text="Зарегистрироваться", font=("Arial", 14),
            bg="#3498db", fg="white", command=self.register
        ).pack(pady=20)

    def register(self):
        """Создание нового пользователя"""
        login = self.entry_login.get().strip()
        p1 = self.entry_password1.get().strip()
        p2 = self.entry_password2.get().strip()

        # Валидация данных: длина логина и пароля
        if not login or not p1 or not p2:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        if len(login) < 4 or len(login) > 16:
            messagebox.showwarning("Ошибка", "Логин должен быть от 4 до 16 символов")
            return

        if p1 != p2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        # Если всё успешно, хешируем пароль и сохраняем в базу
        password_hash = get_hash(p1)
        user_id = data.create_user(login, password_hash)

        if user_id is None:
            messagebox.showerror("Ошибка", "Логин уже существует")
            return

        messagebox.showinfo("Успех", f"Аккаунт создан!\nID счёта: {user_id}")
        self.window.destroy() # Закрываем окно регистрации

# --- ТОЧКА ВХОДА В ПРОГРАММУ ---

if __name__ == "__main__":
    # Этот блок запускается самым первым при старте файла
    root = tk.Tk()
    LoginWindow(root) # Запускаем окно входа
    root.mainloop()