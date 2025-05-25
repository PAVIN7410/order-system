import tkinter as tk
from tkinter import ttk
import sqlite3

# 2. Создаём окошко интерфейса:
app = tk.Tk()
app.title("Система управления заказами")

# 3. Создаем базу данных и таблицу:
def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_details TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Вызов инициализации базы данных
init_db()


# 4. Создаём поля ввода и надписи:
tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

# 5. Создаём таблицу для отображения заказов:
columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")

for column in columns:
    tree.heading(column, text=column)
tree.pack()

# 6. Определяем функцию добавления заказа
def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    # Вставляем новый заказ с автоматическим статусом "Новый"
    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, ?)",
        (customer_name_entry.get(), order_details_entry.get(), "Новый")
    )

    conn.commit()
    conn.close()

    # Очищаем поля после добавления
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)

    # Обновляем отображение заказов
    view_orders()


# 7. Создаем кнопку добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# 8. Создаем функцию вывода текущих заказов
def view_orders():
    # Очищаем таблицу перед обновлением
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# 9. Отображаем текущие заказы при запуске
view_orders()

# Запускаем главный цикл приложения
app.mainloop()