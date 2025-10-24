import os
import sqlite3
from threading import Lock

class DedupStore:
    def __init__(self, db_path=None):
        default_dir = "/app/data"
        os.makedirs(default_dir, exist_ok=True)

        if db_path is None:
            db_path = os.path.join(default_dir, "dedup_store.db")

        print(f"[DedupStore] Using database at: {db_path}")
        self.db_path = db_path
        self.lock = Lock()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS processed_events (
                    topic TEXT,
                    event_id TEXT,
                    PRIMARY KEY (topic, event_id)
                )
            """)

    def is_duplicate(self, topic: str, event_id: str) -> bool:
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT 1 FROM processed_events WHERE topic=? AND event_id=?",
                (topic, event_id),
            )
            return cur.fetchone() is not None

    def add_event(self, topic: str, event_id: str):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO processed_events (topic, event_id) VALUES (?, ?)",
                (topic, event_id),
            )
