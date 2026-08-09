"""
==========================================================
MyFinance

Database Seed Data

Responsibilities
----------------
- Insert initial master data
- Safe to run multiple times
- No business logic
==========================================================
"""

import sqlite3

from config import Config


# ==========================================================
# Master Data
# ==========================================================

STORES = [

    "Alfamart",
    "Indomaret",
    "Supermarket",
    "Traditional Market",
    "Restaurant",
    "Cafe",
    "Online Store",
    "Other",

]


PAYMENT_METHODS = [

    "Cash",
    "Debit Card",
    "Credit Card",
    "Bank Transfer",
    "QRIS",
    "E-Wallet",

]


EXPENSE_CATEGORIES = [

    "Food",
    "Transportation",
    "Utilities",
    "Healthcare",
    "Education",
    "Entertainment",
    "Shopping",
    "Office Supplies",
    "Communication",
    "Housing",
    "Insurance",
    "Investment",
    "Tax",
    "Donation",
    "Travel",
    "Other",

]


# ==========================================================
# Helper Functions
# ==========================================================

def insert_master_data(
    connection: sqlite3.Connection,
    table_name: str,
    column_name: str,
    values: list[str],
) -> None:
    """
    Insert master data using INSERT OR IGNORE.
    """

    cursor = connection.cursor()

    sql = f"""
        INSERT OR IGNORE
        INTO {table_name}
        ({column_name})
        VALUES (?)
    """

    cursor.executemany(

        sql,

        [(value,) for value in values],

    )


def seed_database() -> None:
    """
    Populate master tables.
    """

    connection = sqlite3.connect(
        Config.DATABASE_PATH
    )

    try:

        insert_master_data(

            connection,

            "stores",

            "store_name",

            STORES,

        )

        insert_master_data(

            connection,

            "payment_methods",

            "payment_method_name",

            PAYMENT_METHODS,

        )

        insert_master_data(

            connection,

            "expense_categories",

            "category_name",

            EXPENSE_CATEGORIES,

        )

        connection.commit()

    finally:

        connection.close()


def print_summary() -> None:
    """
    Display record counts.
    """

    connection = sqlite3.connect(
        Config.DATABASE_PATH
    )

    cursor = connection.cursor()

    tables = [

        ("stores", "Stores"),

        ("payment_methods", "Payment Methods"),

        ("expense_categories", "Expense Categories"),

    ]

    print("\nSeed Summary")
    print("-" * 40)

    for table, label in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{label:<20} : {count}")

    connection.close()


# ==========================================================
# Main
# ==========================================================

def main() -> None:

    print("=" * 60)
    print("MyFinance Database Seed")
    print("=" * 60)

    seed_database()

    print("\nMaster data inserted successfully.")

    print_summary()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()