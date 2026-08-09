"""
==========================================================
MyFinance

Application Configuration
==========================================================
"""

from pathlib import Path
import secrets


class Config:
    """
    Base application configuration.
    """

    # ======================================================
    # PROJECT PATHS
    # ======================================================

    BASE_DIR = Path(__file__).resolve().parent

    INSTANCE_DIR = BASE_DIR / "instance"

    DATABASE_NAME = "myfinance.db"

    DATABASE_PATH = INSTANCE_DIR / DATABASE_NAME

    STATIC_DIR = BASE_DIR / "static"

    TEMPLATE_DIR = BASE_DIR / "templates"

    # ======================================================
    # FLASK
    # ======================================================

    SECRET_KEY = secrets.token_hex(32)

    DEBUG = True

    TESTING = False

    # ======================================================
    # DATABASE
    # ======================================================

    DATABASE_TIMEOUT = 30

    ENABLE_FOREIGN_KEYS = True

    SQLITE_DETECT_TYPES = True

    # ======================================================
    # APPLICATION
    # ======================================================

    APP_NAME = "MyFinance"

    APP_VERSION = "1.0.0"

    CURRENCY_SYMBOL = "Rp"

    DATE_FORMAT = "%Y-%m-%d"

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    DECIMAL_PLACES = 2

    # ======================================================
    # EXPENSE MODULE
    # ======================================================

    MAX_ITEMS_PER_TRANSACTION = 500

    MAX_NOTE_LENGTH = 1000

    MAX_RECEIPT_NUMBER_LENGTH = 100

    DEFAULT_DISCOUNT = 0.00

    # ======================================================
    # PAGINATION
    # ======================================================

    DEFAULT_PAGE_SIZE = 20

    MAX_PAGE_SIZE = 100

    # ======================================================
    # LOGGING
    # ======================================================

    LOG_LEVEL = "INFO"

    LOG_FILE = BASE_DIR / "logs" / "myfinance.log"