import tkinter as tk
from tkinter import messagebox
import data
import hashlib

# ИНИЦИАЛИЗАЦИЯ БД ПРИ СТАРТЕ
data.init()


# ПРОВЕРКА БЕЗОПАСНОСТИ ВВОДА
def check_safety(text):
	forbidden_chars = "/^:;\"'--*"
	for char in forbidden_chars:
		if char in text:
			return False
	return True

# ХЕШИРОВАНИЕ ПОРОЛЯ
def get_hash(password):
	password_in_bytes = password.encode('utf-8')
	hash_object = hashlib.sha256(password_in_bytes)
	hex_result = hash_object.hexdigest()
	return hex_result

# ВХОД В СИСТЕМУ
class BankApp:
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
		self.root.geometry(f"{width}x{height}+{x}+{y}")

	def create_widgets(self):
		tk.Label(self.root, text="Логин:", font=("Arial", 18)).grid(row=0, column=0, sticky="e", pady=15)
		self.entry_user = tk.Entry(self.root, font=("Arial", 14), width=20)
		self.entry_user.grid(row=0, column=1, sticky="w", pady=15, padx=(5, 0))

		tk.Label(self.root, text="Пароль:", font=("Arial", 18)).grid(row=1, column=0, sticky="e", pady=10)
		self.entry_pass = tk.Entry(self.root, show="*", font=("Arial", 14), width=20)
		self.entry_pass.grid(row=1, column=1, sticky="w", pady=10, padx=(5, 0))

		self.btn_login = tk.Button(
			self.root,
			text="Войти",
			width=15,
			bg="#2ecc71",
			fg="white",
			font=("Arial", 14, "bold"),
			command=self.login_handler
		)
		self.btn_login.grid(row=2, column=0, columnspan=2, pady=25)

		self.btn_register = tk.Button(
			self.root,
			text="Создать аккаунт",
			width=20,
			bg="lightgrey",
			font=("Arial", 12),
			command=self.open_registration
		)
		self.btn_register.grid(row=3, column=0, columnspan=2)

	def login_handler(self):
		u = self.entry_user.get()
		p = self.entry_pass.get()

		if not check_safety(u) or not check_safety(p):
			messagebox.showerror("Ошибка", "Обнаружены запрещённые символы!")
			return

		if not u or not p:
			messagebox.showwarning("Внимание", "Заполните все поля!")
			return

		if len(u) < 4 or len(u) > 16:
			messagebox.showwarning("Внимание", "Логин должен быть от 4 до 16 символов")
			return

		if len(p) < 4 or len(p) > 16:
			messagebox.showwarning("Внимание", "Пароль должен быть от 4 до 16 символов")
			return

		# ХЕШИРУЕМ ПОРОЛЬ
		current_hash = get_hash(p)
		# ОТПРАВКА В БАЗУ ДАННЫХ (не сделано)

	def open_registration(self):
		RegisterWindow(self.root)

# РЕГИСТРАЦИЯ В СИСТЕМУ
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

		self.btn_create = tk.Button(
			self.window,
			text="Зарегистрироваться",
			width=20,
			bg="#2ecc71",
			fg="white",
			font=("Arial", 14, "bold"),
			command=self.register_handler
		)
		self.btn_create.grid(row=3, column=0, columnspan=2, pady=30)

	def register_handler(self):
		u = self.entry_user_reg.get()
		p1 = self.entry_pass_reg.get()
		p2 = self.entry_pass_repeat.get()

		if not check_safety(u) or not check_safety(p1):
			messagebox.showerror("Ошибка", "Использованы запрещённые символы")
			return

		if not u or not p1 or not p2:
			messagebox.showwarning("Внимание", "Заполните все поля!")
			return

		if len(u) < 4 or len(u) > 16:
			messagebox.showwarning("Внимание", "Логин должен быть от 4 до 16 символов")
			return

		if len(p1) < 4 or len(p1) > 16:
			messagebox.showwarning("Внимание", "Пароль должен быть от 4 до 16 символов")
			return

		if p1 != p2:
			messagebox.showerror("Ошибка", "Пароли не совпадают!")
			return

		# ХЕШИРУЕМ ПОРОЛЬ
		current_hash1 = get_hash(p1)
		# ОТПРАВКА В БАЗУ ДАННЫХ (не сделано)

		# СОЗДАНИЕ СЧЁТА
		account_id = hash(u) & 0x7FFFFFFF
		initial_balance = 0

		data.save_account(account_id, initial_balance)

		messagebox.showinfo(
			"Успех",
			f"Аккаунт создан!\nID счёта: {account_id}"
		)
		self.window.destroy()

if __name__ == "__main__":
	root = tk.Tk()
	app = BankApp(root)
	root.mainloop()
