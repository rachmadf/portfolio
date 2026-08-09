"""
==========================================================
MyFinance

SQLite Database Manager
==========================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

from config import Config

DATABASE_DIR = Config.INSTANCE_DIR

DATABASE_FILE = Config.DATABASE_PATH


# ==========================================================
# INITIALIZATION
# ==========================================================

def initialize_database() -> None:
    """
    Ensure the database directory exists.
    """

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ==========================================================
# CONNECTION
# ==========================================================

def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection.

    Returns
    -------
    sqlite3.Connection
    """

    initialize_database()

    detect_types = 0

    if Config.SQLITE_DETECT_TYPES:
        detect_types = (
            sqlite3.PARSE_DECLTYPES
            | sqlite3.PARSE_COLNAMES
        )

    connection = sqlite3.connect(
        DATABASE_FILE,
        timeout=Config.DATABASE_TIMEOUT,
        detect_types=detect_types,
    )

    connection.row_factory = sqlite3.Row

    if Config.ENABLE_FOREIGN_KEYS:
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

    return connection


# ==========================================================
# CONTEXT MANAGER
# ==========================================================

@contextmanager
def get_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """
    Automatic transaction handling.

    Example
    -------
    with get_cursor() as cursor:
        cursor.execute(...)
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        yield cursor

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()

        connection.close()


# ==========================================================
# TRANSACTION
# ==========================================================

@contextmanager
def transaction() -> Generator[sqlite3.Connection, None, None]:
    """
    Manual transaction handling.

    Example
    -------
    with transaction() as conn:

        cursor = conn.cursor()

        cursor.execute(...)
    """

    connection = get_connection()

    try:

        yield connection

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ==========================================================
# TEST CONNECTION
# ==========================================================

def test_connection() -> bool:
    """
    Verify database connectivity.
    """

    try:

        with get_connection() as connection:

            connection.execute("SELECT 1")

        return True

    except Exception:

        return False