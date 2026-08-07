from pathlib import Path
from datetime import datetime

from src.database.database import get_connection

class MetadataDatabase:

    def __init__(self):

        # self.connection = None
        self.connect()

    def connect(self):
        if hasattr(self, "connection") and self.connection:
            self.connection.close()

        self.connection = get_connection()

        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pages (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                page_type TEXT NOT NULL,

                path TEXT NOT NULL UNIQUE,

                last_modified TEXT NOT NULL,

                vector_id INTEGER UNIQUE
            )
            """
        )

        self.connection.commit()

    def upsert_page(
    self,
    page_path,
    title,
    page_type
):

        page_path = Path(page_path)

        modified = datetime.fromtimestamp(
            page_path.stat().st_mtime
        ).isoformat()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO pages
            (
                title,
                page_type,
                path,
                last_modified
            )

            VALUES
            (?, ?, ?, ?)

            ON CONFLICT(path)

            DO UPDATE SET

                title=excluded.title,

                page_type=excluded.page_type,

                last_modified=excluded.last_modified
            """,
            (
                title,
                page_type,
                str(page_path),
                modified
            )
        )

        # --------------------------------------------------
        # Assign a permanent vector_id if this page doesn't
        # already have one.
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT vector_id
            FROM pages
            WHERE path=?
            """,
            (
                str(page_path),
            )
        )

        row = cursor.fetchone()

        if row and row[0] is None:

            cursor.execute(
                """
                SELECT MAX(vector_id)
                FROM pages
                """
            )

            result = cursor.fetchone()[0]

            next_id = 1 if result is None else result + 1

            cursor.execute(
                """
                UPDATE pages
                SET vector_id=?
                WHERE path=?
                """,
                (
                    next_id,
                    str(page_path)
                )
            )

        self.connection.commit()

    def fetch_all_pages(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                title,
                page_type,
                path,
                last_modified
            FROM pages
            """
        )

        return cursor.fetchall()
    
    def get_page(self, path):

        cursor = self.connection.cursor()

        cursor.execute(

            """
            SELECT
                title,
                page_type,
                path,
                last_modified
            FROM pages
            WHERE path = ?
            """,

            (path,)

        )

        return cursor.fetchone()
    
    def initialize_vector_ids(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id
            FROM pages
            WHERE vector_id IS NULL
            ORDER BY id
        """)

        rows = cursor.fetchall()

        next_id = 1

        cursor.execute("""
            SELECT MAX(vector_id)
            FROM pages
        """)

        result = cursor.fetchone()[0]

        if result is not None:
            next_id = result + 1

        for row in rows:

            cursor.execute(
                """
                UPDATE pages
                SET vector_id=?
                WHERE id=?
                """,
                (
                    next_id,
                    row[0]
                )
            )

            next_id += 1

        self.connection.commit()

    def get_vector_id(self, path):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT vector_id
            FROM pages
            WHERE path=?
            """,
            (
                str(path),
            )
        )

        row = cursor.fetchone()

        if row:

            return row[0]

        return None
    
    
metadata_db = MetadataDatabase()