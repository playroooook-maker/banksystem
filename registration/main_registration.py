import tkinter as tk
from tkinter import messagebox


# 1. Выносим проверку в отдельную функцию, чтобы использовать её везде
def check_safety(text):
    forbidden_chars = "/^:;\"'--*"
    for char in forbidden_chars:
        if char in text:
            return False
    return True


class BankApp:
    # ... (код __init__ и center_window остается прежним)
    def __init__(self, root):
        self.root = root
        self.root.title("SberPython Bank")
        self.root.resizable(False, False)
        self.center_window(500, 280)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        tk.Label(self.root, text="Логин:", font=("Arial", 18)).grid(row=0, column=0, sticky="e", pady=15)
        self.entry_user = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.entry_user.grid(row=0, column=1, sticky="w", pady=15, padx=(5, 0))

        tk.Label(self.root, text="Пароль:", font=("Arial", 18)).grid(row=1, column=0, sticky="e", pady=10)
        self.entry_pass = tk.Entry(self.root, show="*", font=("Arial", 14), width=20)
        self.entry_pass.grid(row=1, column=1, sticky="w", pady=10, padx=(5, 0))

        self.btn_login = tk.Button(self.root, text="Войти", width=15, bg="#2ecc71", fg="white",
                                   font=("Arial", 14, "bold"), command=self.login_handler)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=25)

        self.btn_register = tk.Button(self.root, text="Создать аккаунт", width=20, bg="lightgrey", font=("Arial", 12),
                                      command=self.open_registration)
        self.btn_register.grid(row=3, column=0, columnspan=2)

    def login_handler(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        # ЗАЩИТА НА ВХОДЕ
        if not check_safety(u) or not check_safety(p):
            messagebox.showerror("Ошибка", "Обнаружены запрещенные символы!")
            return

        if not u or not p:
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        elif len(u) <= 3 or len(u) >= 17:
            messagebox.showwarning("Внимание", "Длина логина не должна быть меньше 4 и больше 16")

        elif len(p) <= 3 or len(p) >= 17:
            messagebox.showwarning("Внимание", "Длина пароля не должна быть меньше 4 и больше 16")


        print(f"Пытаемся войти: {u}")

    def open_registration(self):
        RegisterWindow(self.root)


class RegisterWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Регистрация")
        self.window.geometry("500x300")
        self.window.resizable(False, False)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.create_widgets_reg()

    def create_widgets_reg(self):
        tk.Label(self.window, text="Логин:", font=("Arial", 16)).grid(row=0, column=0, sticky="e", pady=15)
        self.entry_user_reg = tk.Entry(self.window, font=("Arial", 14), width=20)
        self.entry_user_reg.grid(row=0, column=1, sticky="w", pady=15, padx=(5, 0))

        tk.Label(self.window, text="Пароль:", font=("Arial", 16)).grid(row=1, column=0, sticky="e", pady=10)
        self.entry_pass_reg = tk.Entry(self.window, show="*", font=("Arial", 14), width=20)
        self.entry_pass_reg.grid(row=1, column=1, sticky="w", pady=10, padx=(5, 0))

        tk.Label(self.window, text="Повтор:", font=("Arial", 16)).grid(row=2, column=0, sticky="e", pady=10)
        self.entry_pass_repeat = tk.Entry(self.window, show="*", font=("Arial", 14), width=20)
        self.entry_pass_repeat.grid(row=2, column=1, sticky="w", pady=10, padx=(5, 0))

        self.btn_create = tk.Button(self.window, text="Зарегистрироваться", width=20, bg="#2ecc71", fg="white",
                                    font=("Arial", 14, "bold"), command=self.register_handler)
        self.btn_create.grid(row=3, column=0, columnspan=2, pady=30)

    def register_handler(self):
        u = self.entry_user_reg.get()
        p1 = self.entry_pass_reg.get()
        p2 = self.entry_pass_repeat.get()

        # ЗАЩИТА НА РЕГИСТРАЦИИ
        if not check_safety(u) or not check_safety(p1):
            messagebox.showerror("Ошибка", "Использованы запрещенные символы /^:;\"'--*")
            return

        if p1 != p2:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
        elif not u or not p1:
            messagebox.showwarning("Внимание", "Заполните все поля!")
        elif len(u) <= 3 or len(u) >= 17:
            messagebox.showwarning("Внимание", "Длина логина не должна быть меньше 4 и больше 16")
        elif len(p1) <= 3 or len(p1) >= 17:
            messagebox.showwarning("Внимание", "Длина пароля не должна быть меньше 4 и больше 16")
        else:
            messagebox.showinfo("Успех", f"Аккаунт {u} создан!")
            self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()