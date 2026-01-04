import tkinter as tk
from tkinter import messagebox
import hashlib
import data
# ИНИЦИАЛИЗАЦИЯ БД
data.init_db()
# УТИЛИТЫ
def check_safety(text: str) -> bool:
    forbidden = "/^:;\"'--*"
    return not any(c in forbidden for c in text)


def get_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
# ОКНО ВХОДА
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank | Вход")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        tk.Label(root, text="Логин", font=("Arial", 14)).pack(pady=10)
        self.entry_login = tk.Entry(root, font=("Arial", 14))
        self.entry_login.pack()

        tk.Label(root, text="Пароль", font=("Arial", 14)).pack(pady=10)
        self.entry_password = tk.Entry(root, show="*", font=("Arial", 14))
        self.entry_password.pack()

        tk.Button(
            root,
            text="Войти",
            font=("Arial", 14),
            bg="#2ecc71",
            fg="white",
            command=self.login
        ).pack(pady=15)

        tk.Button(
            root,
            text="Создать аккаунт",
            font=("Arial", 12),
            command=self.open_register
        ).pack()

    def login(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        if not check_safety(login) or not check_safety(password):
            messagebox.showerror("Ошибка", "Запрещённые символы")
            return

        password_hash = get_hash(password)
        user_id = data.check_login(login, password_hash)

        if user_id is None:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            return

        self.root.destroy()
        open_main_window(user_id)

    def open_register(self):
        RegisterWindow(self.root)

# ОКНО РЕГИСТРАЦИИ
class RegisterWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Регистрация")
        self.window.geometry("420x320")
        self.window.resizable(False, False)

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
            self.window,
            text="Зарегистрироваться",
            font=("Arial", 14),
            bg="#3498db",
            fg="white",
            command=self.register
        ).pack(pady=20)

    def register(self):
        login = self.entry_login.get().strip()
        p1 = self.entry_password1.get().strip()
        p2 = self.entry_password2.get().strip()

        if not login or not p1 or not p2:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        if not check_safety(login) or not check_safety(p1):
            messagebox.showerror("Ошибка", "Запрещённые символы")
            return

        if len(login) < 4 or len(login) > 16:
            messagebox.showwarning("Ошибка", "Логин 4–16 символов")
            return

        if len(p1) < 4 or len(p1) > 16:
            messagebox.showwarning("Ошибка", "Пароль 4–16 символов")
            return

        if p1 != p2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        password_hash = get_hash(p1)
        user_id = data.create_user(login, password_hash)

        if user_id is None:
            messagebox.showerror("Ошибка", "Логин уже существует")
            return

        messagebox.showinfo(
            "Успех",
            f"Аккаунт создан!\nID счёта: {user_id}"
        )
        self.window.destroy()
# ГЛАВНОЕ ОКНО ПОЛЬЗОВАТЕЛЯ
def open_main_window(user_id: int):
    root = tk.Tk()
    root.title("Bank | Аккаунт")
    root.geometry("420x300")
    root.resizable(False, False)

    balance_label = tk.Label(root, font=("Arial", 16))
    balance_label.pack(pady=20)

    def refresh_balance():
        balance = data.get_balance(user_id)
        balance_label.config(text=f"Баланс: {balance}")

    refresh_balance()

    tk.Label(root, text="ID получателя", font=("Arial", 12)).pack()
    entry_to = tk.Entry(root, font=("Arial", 12))
    entry_to.pack()

    tk.Label(root, text="Сумма", font=("Arial", 12)).pack(pady=5)
    entry_amount = tk.Entry(root, font=("Arial", 12))
    entry_amount.pack()

    def do_transfer():
        try:
            to_id = int(entry_to.get())
            amount = int(entry_amount.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа")
            return

        result = data.transfer(user_id, to_id, amount)

        if result == 0:
            messagebox.showinfo("Успех", "Перевод выполнен")
            refresh_balance()
        elif result == -1:
            messagebox.showerror("Ошибка", "Некорректная сумма")
        elif result == -2:
            messagebox.showerror("Ошибка", "Ваш счёт не найден")
        elif result == -3:
            messagebox.showerror("Ошибка", "Получатель не найден")
        elif result == -4:
            messagebox.showerror("Ошибка", "Недостаточно средств")
        else:
            messagebox.showerror("Ошибка", "Неизвестная ошибка")

    tk.Button(
        root,
        text="Перевести",
        font=("Arial", 14),
        bg="#2ecc71",
        fg="white",
        command=do_transfer
    ).pack(pady=20)

    root.mainloop()
# ТОЧКА ВХОДА
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
