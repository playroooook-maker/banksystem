import tkinter as tk
from tkinter import messagebox
import data
import hashlib

# ИНИЦИАЛИЗАЦИЯ БД
data.init()


def check_safety(text):
    forbidden_chars = "/^:;\"'--*"
    for char in forbidden_chars:
        if char in text:
            return False
    return True


def get_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SberPython Bank")
        self.root.resizable(False, False)
        self.center_window(500, 280)
        self.create_widgets()

    def center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        tk.Label(self.root, text="Логин:", font=("Arial", 18)).grid(row=0, column=0, pady=15)
        self.entry_user = tk.Entry(self.root, font=("Arial", 14))
        self.entry_user.grid(row=0, column=1)

        tk.Label(self.root, text="Пароль:", font=("Arial", 18)).grid(row=1, column=0)
        self.entry_pass = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.entry_pass.grid(row=1, column=1)

        tk.Button(
            self.root,
            text="Войти",
            font=("Arial", 14),
            bg="#2ecc71",
            fg="white",
            command=self.login_handler
        ).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(
            self.root,
            text="Создать аккаунт",
            command=self.open_registration
        ).grid(row=3, column=0, columnspan=2)

    def login_handler(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        if not check_safety(u) or not check_safety(p):
            messagebox.showerror("Ошибка", "Запрещённые символы")
            return

        password_hash = get_hash(p)
        user = data.check_user_login(u, password_hash)

        if user:
            account_id, balance = user
            messagebox.showinfo(
                "Успех",
                f"Вход выполнен!\nID: {account_id}\nБаланс: {balance}"
            )
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def open_registration(self):
        RegisterWindow(self.root)


class RegisterWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Регистрация")
        self.window.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Логин:", font=("Arial", 16)).grid(row=0, column=0, pady=15)
        self.entry_user = tk.Entry(self.window, font=("Arial", 14))
        self.entry_user.grid(row=0, column=1)

        tk.Label(self.window, text="Пароль:", font=("Arial", 16)).grid(row=1, column=0)
        self.entry_pass1 = tk.Entry(self.window, show="*", font=("Arial", 14))
        self.entry_pass1.grid(row=1, column=1)

        tk.Label(self.window, text="Повтор:", font=("Arial", 16)).grid(row=2, column=0)
        self.entry_pass2 = tk.Entry(self.window, show="*", font=("Arial", 14))
        self.entry_pass2.grid(row=2, column=1)

        tk.Button(
            self.window,
            text="Зарегистрироваться",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 14),
            command=self.register_handler
        ).grid(row=3, column=0, columnspan=2, pady=25)

    def register_handler(self):
        u = self.entry_user.get()
        p1 = self.entry_pass1.get()
        p2 = self.entry_pass2.get()

        if not u or not p1 or not p2:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        if p1 != p2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        password_hash = get_hash(p1)
        account_id = hash(u) & 0x7FFFFFFF

        try:
            data.create_user(account_id, u, password_hash)
        except Exception:
            messagebox.showerror("Ошибка", "Логин уже существует")
            return

        messagebox.showinfo(
            "Успех",
            f"Аккаунт создан!\nID счёта: {account_id}"
        )
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
