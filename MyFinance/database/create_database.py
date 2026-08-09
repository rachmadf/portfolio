"""
MyFinance
Database Initialization Script

File    : create_database.py
Version : 1.0
Author  : Rachmad Fitriyanto

Description
-----------
Create SQLite database for MyFinance application.

This script will:

1. Create SQLite database
2. Create all required tables
3. Insert default master data
4. Create indexes
5. Enable foreign key support

Safe to execute multiple times.
"""

import sqlite3
from pathlib import Path


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_DIR = Path(__file__).parent
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "myfinance.db"


# ==========================================================
# CONNECT DATABASE
# ==========================================================

connection = sqlite3.connect(DATABASE_PATH)

connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

print("=" * 70)
print("MYFINANCE DATABASE INITIALIZATION")
print("=" * 70)


# ==========================================================
# STORE TABLE
# ==========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS stores
(

    store_id INTEGER PRIMARY KEY AUTOINCREMENT,

    store_name TEXT NOT NULL UNIQUE,

    address TEXT,

    phone TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

""")


# ==========================================================
# PAYMENT METHOD
# ==========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS payment_methods
(

    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,

    payment_method_name TEXT NOT NULL UNIQUE,

    description TEXT,

    is_active INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

""")


# ==========================================================
# EXPENSE CATEGORY
# ==========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS expense_categories
(

    category_id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT NOT NULL UNIQUE,

    description TEXT,

    is_active INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

""")


# ==========================================================
# EXPENSE TRANSACTION (HEADER)
# ==========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS expense_transactions
(

    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,

    receipt_no TEXT NOT NULL UNIQUE,

    transaction_date DATE NOT NULL,

    store_id INTEGER NOT NULL,

    payment_method_id INTEGER NOT NULL,

    discount_amount REAL DEFAULT 0 CHECK(discount_amount >= 0),

    total_amount REAL NOT NULL CHECK(total_amount >= 0),

    notes TEXT,

    receipt_image TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted INTEGER DEFAULT 0,

    FOREIGN KEY(store_id)
        REFERENCES stores(store_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY(payment_method_id)
        REFERENCES payment_methods(payment_method_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

);

""")


# ==========================================================
# EXPENSE DETAIL
# ==========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS expense_details
(

    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,

    expense_id INTEGER NOT NULL,

    category_id INTEGER NOT NULL,

    item_name TEXT NOT NULL,

    brand TEXT,

    size TEXT,

    quantity REAL NOT NULL CHECK(quantity > 0),

    unit_price REAL NOT NULL CHECK(unit_price >= 0),

    subtotal REAL NOT NULL CHECK(subtotal >= 0),

    FOREIGN KEY(expense_id)
        REFERENCES expense_transactions(expense_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY(category_id)
        REFERENCES expense_categories(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

);

""")


# ==========================================================
# INDEXES
# ==========================================================

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_expense_date

ON expense_transactions(transaction_date)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_store

ON expense_transactions(store_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_expense_detail

ON expense_details(expense_id)

""")

cursor.execute("""

CREATE INDEX IF NOT EXISTS idx_category

ON expense_details(category_id)

""")


# ==========================================================
# DEFAULT PAYMENT METHODS
# ==========================================================

payment_methods = [

("Cash","Cash Payment"),

("Debit Card","Debit Card"),

("Credit Card","Credit Card"),

("Bank Transfer","Transfer"),

("QRIS","QRIS"),

("GoPay","GoPay"),

("OVO","OVO"),

("DANA","DANA"),

("ShopeePay","ShopeePay")

]

cursor.executemany("""

INSERT OR IGNORE INTO payment_methods
(payment_method_name,description)

VALUES (?,?)

""", payment_methods)


# ==========================================================
# DEFAULT STORES
# ==========================================================

stores = [

("MM Permata Pagar Drum","",""),

("Lazatto Pagar Drum","",""),

("Indomaret","",""),

("Alfamart","",""),

("Hypermart","",""),

("Super Indo","",""),

("Shopee","",""),

("Tokopedia","",""),

("GrabFood","",""),

("GoFood","","")

]

cursor.executemany("""

INSERT OR IGNORE INTO stores

(store_name,address,phone)

VALUES (?,?,?)

""", stores)


# ==========================================================
# DEFAULT CATEGORIES
# ==========================================================

categories = [

("Bahan Makanan",""),

("Paket Makanan",""),

("Snack",""),

("Minuman",""),

("Rumah Tangga",""),

("Transportasi",""),

("Listrik",""),

("Air",""),

("Internet",""),

("Pulsa",""),

("Pendidikan",""),

("Kesehatan",""),

("Pakaian",""),

("Hiburan",""),

("Otomotif",""),

("Perawatan Pribadi",""),

("Hadiah",""),

("Lainnya","")

]

cursor.executemany("""

INSERT OR IGNORE INTO expense_categories

(category_name,description)

VALUES (?,?)

""", categories)


# ==========================================================
# COMMIT
# ==========================================================

connection.commit()


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

print()

print("Database Location")

print(DATABASE_PATH)

print()

tables = cursor.execute("""

SELECT name

FROM sqlite_master

WHERE type='table'

ORDER BY name

""").fetchall()

print("Tables")

for table in tables:

    print(f"  ✓ {table[0]}")

print()

print("Payment Methods :", cursor.execute(
"SELECT COUNT(*) FROM payment_methods").fetchone()[0])

print("Stores          :", cursor.execute(
"SELECT COUNT(*) FROM stores").fetchone()[0])

print("Categories      :", cursor.execute(
"SELECT COUNT(*) FROM expense_categories").fetchone()[0])

connection.close()

print()

print("=" * 70)

print("DATABASE CREATED SUCCESSFULLY")

print("=" * 70)