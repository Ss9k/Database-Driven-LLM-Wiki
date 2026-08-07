from pathlib import Path
import sqlite3

from src.workspace.workspace import workspace

DATABASE_PATH = Path("data/database")

DATABASE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

DB_FILE = DATABASE_PATH / "metadata.db"


def get_connection():

    return sqlite3.connect(
        workspace.database,
        check_same_thread=False
    )