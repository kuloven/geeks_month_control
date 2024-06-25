import sqlite3

def initialize_database():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        code VARCHAR(2) PRIMARY KEY,
        title VARCHAR(150)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title VARCHAR(250),
        category_code VARCHAR(2),
        unit_price FLOAT,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY (category_code) REFERENCES categories (code),
        FOREIGN KEY (store_id) REFERENCES store (store_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS store (
        store_id INTEGER PRIMARY KEY,
        title VARCHAR(100)
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        categories = [
            ('FD', 'Food products'),
            ('EL', 'Electronics'),
            ('CL', 'Clothes')
        ]
        cursor.executemany('INSERT INTO categories (code, title) VALUES (?, ?)', categories)

    cursor.execute('SELECT COUNT(*) FROM store')
    if cursor.fetchone()[0] == 0:
        stores = [
            (1, 'Asia'),
            (2, 'Globus'),
            (3, 'Spar')
        ]
        cursor.executemany('INSERT INTO store (store_id, title) VALUES (?, ?)', stores)

    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        products = [
            (1, 'Chocolate', 'FD', 10.5, 129, 1),
            (2, 'Jeans', 'CL', 120.0, 55, 2),
            (3, 'T-Shirt', 'CL', 460.0, 15, 1),
            (4, 'Laptop', 'EL', 999.99, 20, 3),
            (5, 'Smartphone', 'EL', 499.99, 50, 3)
        ]
        cursor.executemany('INSERT INTO products (id, title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?, ?)', products)

    conn.commit()
    conn.close()

def get_stores():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT store_id, title FROM store')
    stores = cursor.fetchall()
    conn.close()
    return stores

def get_products_by_store(store_id):
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT p.title, c.title, p.unit_price, p.stock_quantity
    FROM products p
    JOIN categories c ON p.category_code = c.code
    WHERE p.store_id = ?
    ''', (store_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def main():
    initialize_database()

    print("Вы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже\n"
          "(для выхода из программы введите цифру 0:)")

    stores = get_stores()
    for store in stores:
        print(f"{store[0]}. {store[1]}")

    while True:
        try:
            store_id = int(input("Введите id магазина: "))
        except ValueError:
            print("Пожалуйста, введите корректный id магазина.")
            continue

        if store_id == 0:
            break

        products = get_products_by_store(store_id)
        if products:
            for product in products:
                print(f"Название продукта: {product[0]}")
                print(f"Категория: {product[1]}")
                print(f"Цена: {product[2]}")
                print(f"Количество на складе: {product[3]}")
                print()
        else:
            print("Нет продуктов для данного магазина.\n")

if __name__ == "__main__":
    main()
