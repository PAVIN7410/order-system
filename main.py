import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

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

def complete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()

        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))

        conn.commit()
        conn.close()

        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")


# 7. Создаем кнопку добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# 8.Создаем кнопку завершения заказа
complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()

# 9. Создаем функцию вывода текущих заказов
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

# 10. Создаем функцию завершения заказа по ID  Отображаем текущие заказы при запуске
view_orders()

# Запускаем главный цикл приложения
app.mainloop()