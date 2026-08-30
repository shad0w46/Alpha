import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path):
        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.path
        )

    def initialize(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                enabled INTEGER DEFAULT 1
            )
        """)

        self.connection.commit()

    def add_event(self, event_type, message):
        self.connection.execute(
            """
            INSERT INTO events (
                event_type,
                message
            )
            VALUES (?, ?)
            """,
            (
                event_type,
                message
            )
        )

        self.connection.commit()

    def register_module(
        self,
        module_id,
        name,
        version
    ):
        self.connection.execute(
            """
            INSERT OR REPLACE INTO modules (
                id,
                name,
                version,
                enabled
            )
            VALUES (?, ?, ?, 1)
            """,
            (
                module_id,
                name,
                version
            )
        )

        self.connection.commit()

    def get_modules(self):
        cursor = self.connection.execute("""
            SELECT
                id,
                name,
                version,
                enabled
            FROM modules
            ORDER BY id
        """)

        return cursor.fetchall()

    def close(self):
        self.connection.close()
