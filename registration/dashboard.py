import tkinter as tk
from tkinter import ttk, messagebox
import data  # Импортируем наш файл с логикой базы данных

# Проверяем в консоли, подгрузились ли все нужные функции из data.py
print("Список функций в файле data:", dir(data))


class DashboardApp:
    def __init__(self, user_id):
        # Сохраняем ID вошедшего пользователя, чтобы знать, чей это личный кабинет
        self.user_id = user_id

        # Создаем основное окно
        self.root = tk.Tk()
        self.root.title("SberPython | Личный кабинет")
        self.root.geometry("700x500")
        self.root.resizable(False, False)  # Запрещаем менять размер окна, чтобы дизайн не "поплыл"

        # --- НАСТРОЙКА ВНЕШНЕГО ВИДА ТАБЛИЦЫ ---
        style = ttk.Style()
        # "Treeview" — это системное название виджета таблицы в Tkinter
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        # Настраиваем шрифт только для заголовков столбцов
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Вызываем методы отрисовки интерфейса и загрузки данных
        self.create_widgets()
        self.refresh_data()

        # Запускаем бесконечный цикл окна (чтобы оно не закрылось сразу)
        self.root.mainloop()

    def create_widgets(self):
        """Метод, который 'рисует' кнопки, поля и надписи на экране"""

        # --- ВЕРХНЯЯ ЗЕЛЕНАЯ ПАНЕЛЬ С БАЛАНСОМ ---
        # Frame — это просто 'рамка' или контейнер для других элементов
        header_frame = tk.Frame(self.root, bg="#2ecc71", height=80)
        header_frame.pack(fill="x")  # Растягиваем по горизонтали (ось X)

        self.label_balance = tk.Label(
            header_frame,
            text="Баланс: 0 руб.",
            font=("Arial", 20, "bold"),
            bg="#2ecc71", fg="white"  # Белый текст на зеленом фоне
        )
        self.label_balance.pack(pady=20)

        # --- ОБЩИЙ КОНТЕНТ (ниже баланса) ---
        main_content = tk.Frame(self.root)
        main_content.pack(fill="both", expand=True, padx=20, pady=10)

        # --- ЛЕВАЯ ЧАСТЬ: ФОРМА ПЕРЕВОДА ---
        # LabelFrame — рамка с заголовком вокруг элементов
        transfer_frame = tk.LabelFrame(main_content, text="Новый перевод", font=("Arial", 12, "bold"), padx=10, pady=10)
        transfer_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(transfer_frame, text="Логин получателя:").pack(anchor="w")
        self.entry_to_user = tk.Entry(transfer_frame, font=("Arial", 12))
        self.entry_to_user.pack(fill="x", pady=5)

        tk.Label(transfer_frame, text="Сумма:").pack(anchor="w")
        self.entry_amount = tk.Entry(transfer_frame, font=("Arial", 12))
        self.entry_amount.pack(fill="x", pady=5)

        # Кнопка вызывает функцию self.send_money при нажатии
        tk.Button(
            transfer_frame, text="Отправить деньги",
            bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
            command=self.send_money
        ).pack(fill="x", pady=15)

        # --- ПРАВАЯ ЧАСТЬ: ИСТОРИЯ (ТАБЛИЦА) ---
        history_frame = tk.LabelFrame(main_content, text="История транзакций", font=("Arial", 12, "bold"), padx=10,
                                      pady=10)
        history_frame.pack(side="right", fill="both", expand=True)

        # Настраиваем столбцы таблицы
        columns = ("date", "target", "amount")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)

        # Текст в заголовках
        self.tree.heading("date", text="Дата")
        self.tree.heading("target", text="Пользователь")
        self.tree.heading("amount", text="Сумма")

        # Ширина столбцов в пикселях
        self.tree.column("date", width=120)
        self.tree.column("target", width=100)
        self.tree.column("amount", width=80)

        self.tree.pack(fill="both", expand=True)

    def refresh_data(self):
        """Функция обновления баланса и таблицы из БД (вызывается при входе и после перевода)"""

        # 1. Запрашиваем баланс из data.py по нашему ID
        balance = data.get_balance(self.user_id)
        # Меняем текст в верхней лейбле
        self.label_balance.config(text=f"Баланс: {balance} руб.")

        # 2. Очищаем таблицу от старых записей (чтобы данные не дублировались)
        for i in self.tree.get_children():
            self.tree.delete(i)

        # 3. Берем свежую историю из базы (получаем список кортежей)
        history = data.get_transaction_history(self.user_id)
        for row in history:
            # Вставляем строку в конец таблицы Treeview
            self.tree.insert("", "end", values=row)

    def send_money(self):
        """Логика обработки нажатия на кнопку 'Отправить'"""

        # Считываем данные из полей ввода
        target_login = self.entry_to_user.get().strip()  # .strip() убирает лишние пробелы по краям

        try:
            # Пробуем превратить введенную сумму в целое число
            amount = int(self.entry_amount.get())

            # Твоя проверка на лимит в 10 миллионов
            if amount > 10_000_000:
                messagebox.showerror("Ошибка", "Максимальная сумма перевода: 10 000 000 руб.")
                return  # Прерываем функцию

        except ValueError:
            # Если в поле суммы ввели буквы, сработает этот блок
            messagebox.showerror("Ошибка", "Введите корректную сумму цифрами")
            return

        # Отправляем данные в data.py и получаем цифровой код результата
        result = data.transfer_by_login(self.user_id, target_login, amount)

        if result == 0:
            # Если всё успешно (код 0)
            messagebox.showinfo("Успех", f"Перевод {amount} руб. пользователю {target_login} выполнен!")
            self.refresh_data()  # Перерисовываем баланс и таблицу

            # Очищаем поля ввода, чтобы они стали пустыми после отправки
            self.entry_to_user.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
        else:
            # Если возникла ошибка, берем понятный текст из словаря по коду (result)
            errors = {
                -1: "Неверная сумма",
                -2: "Ваш счет не найден",
                -3: "Получатель не найден",
                -4: "Недостаточно средств",
                -6: "Превышен лимит в 10 000 000 руб."
            }
            # Показываем текст ошибки или "Неизвестная ошибка", если кода нет в словаре
            messagebox.showerror("Ошибка", errors.get(result, "Ошибка на стороне сервера"))