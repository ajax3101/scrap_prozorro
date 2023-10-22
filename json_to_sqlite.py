import sqlite3
import json

# Откройте JSON-файл для чтения
with open('data_22_10_2023.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

# Определите имя для SQLite-таблицы (или используйте произвольное имя)
table_name = 'json_data'

# Создайте SQLite-соединение и курсор
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Создайте таблицу с одним столбцом для хранения JSON-данных как текстовой строки
create_table_query = f"CREATE TABLE {table_name} (json_data TEXT);"
cursor.execute(create_table_query)

# Вставьте JSON-данные в SQLite
insert_query = f"INSERT INTO {table_name} (json_data) VALUES (?);"

# Преобразуйте JSON-данные в текстовую строку
json_text = json.dumps(data)

# Выполните вставку
cursor.execute(insert_query, (json_text,))

# Сохраните изменения и закройте соединение
conn.commit()
conn.close()