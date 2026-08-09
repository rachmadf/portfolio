-- ==========================================================
-- MyFinance
-- SQLite Database Schema
-- ==========================================================

PRAGMA foreign_keys = ON;

-- ==========================================================
-- Drop Existing Tables
-- ==========================================================

DROP TABLE IF EXISTS expense_details;
DROP TABLE IF EXISTS expense_transactions;
DROP TABLE IF EXISTS expense_categories;
DROP TABLE IF EXISTS payment_methods;
DROP TABLE IF EXISTS stores;

-- ==========================================================
-- Stores
-- ==========================================================

CREATE TABLE stores (

    store_id INTEGER PRIMARY KEY AUTOINCREMENT,

    store_name TEXT NOT NULL UNIQUE,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0,1))

);

-- ==========================================================
-- Payment Methods
-- ==========================================================

CREATE TABLE payment_methods (

    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,

    payment_method_name TEXT NOT NULL UNIQUE,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0,1))

);

-- ==========================================================
-- Expense Categories
-- ==========================================================

CREATE TABLE expense_categories (

    category_id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT NOT NULL UNIQUE,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0,1))

);

-- ==========================================================
-- Expense Transactions
-- ==========================================================

CREATE TABLE expense_transactions (

    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_date TEXT NOT NULL,

    receipt_number TEXT,

    store_id INTEGER NOT NULL,

    payment_method_id INTEGER NOT NULL,

    note TEXT,

    subtotal REAL NOT NULL DEFAULT 0,

    discount REAL NOT NULL DEFAULT 0,

    total REAL NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    FOREIGN KEY (payment_method_id)
        REFERENCES payment_methods(payment_method_id)

);

-- ==========================================================
-- Expense Details
-- ==========================================================

CREATE TABLE expense_details (

    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_id INTEGER NOT NULL,

    category_id INTEGER NOT NULL,

    item_name TEXT NOT NULL,

    quantity REAL NOT NULL,

    unit_price REAL NOT NULL,

    subtotal REAL NOT NULL,

    FOREIGN KEY (transaction_id)
        REFERENCES expense_transactions(transaction_id)
        ON DELETE CASCADE,

    FOREIGN KEY (category_id)
        REFERENCES expense_categories(category_id)

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_transaction_date
ON expense_transactions(transaction_date);

CREATE INDEX idx_receipt_number
ON expense_transactions(receipt_number);

CREATE INDEX idx_store
ON expense_transactions(store_id);

CREATE INDEX idx_payment_method
ON expense_transactions(payment_method_id);

CREATE INDEX idx_detail_transaction
ON expense_details(transaction_id);

CREATE INDEX idx_detail_category
ON expense_details(category_id);

-- ==========================================================
-- End
-- ==========================================================