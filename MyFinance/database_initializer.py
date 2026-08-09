"""
==========================================================
MyFinance

Database Initializer

Responsibilities
----------------
- Create instance directory
- Create SQLite database
- Execute schema.sql
- Verify required tables
==========================================================
"""

import sqlite3
from pathlib import Path

from config import Config


# ==========================================================
# Constants
# ==========================================================

SCHEMA_FILE = Config.BASE_DIR / "schema.sql"

DATABASE_FILE = Config.DATABASE_PATH

REQUIRED_TABLES = [
    "stores",
    "payment_methods",
    "expense_categories",
    "expense_transactions",
    "expense_details",
]


# ==========================================================
# Helper Functions
# ==========================================================

def create_instance_directory() -> None:
    """
    Create instance directory if it does not exist.
    """

    Config.INSTANCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def load_schema() -> str:
    """
    Load schema.sql.
    """

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_FILE}"
        )

    return SCHEMA_FILE.read_text(
        encoding="utf-8"
    )


def create_database() -> None:
    """
    Execute schema.sql.
    """

    schema = load_schema()

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    try:

        connection.executescript(schema)

        connection.commit()

    finally:

        connection.close()


def verify_database() -> bool:
    """
    Verify required tables exist.
    """

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        )

        existing_tables = {

            row[0]

            for row in cursor.fetchall()

        }

    finally:

        connection.close()

    missing = [

        table

        for table in REQUIRED_TABLES

        if table not in existing_tables

    ]

    if missing:

        print("\nMissing tables:")

        for table in missing:

            print(f"  - {table}")

        return False

    return True


# ==========================================================
# Main
# ==========================================================

def initialize_database() -> bool:
    """
    Initialize SQLite database.
    """

    print("=" * 60)
    print("MyFinance Database Initialization")
    print("=" * 60)

    print("\nCreating instance directory...")

    create_instance_directory()

    print("OK")

    print("\nExecuting schema.sql...")

    create_database()

    print("OK")

    print("\nVerifying database...")

    if verify_database():

        print("OK")

        print("\nDatabase initialized successfully.")

        print(f"\nDatabase location:\n{DATABASE_FILE}")

        return True

    print("FAILED")

    return False


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    success = initialize_database()

    if not success:

        raise SystemExit(1)