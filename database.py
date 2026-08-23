"""SQLite helpers for storing job postings in postings.db."""

import sqlite3
from datetime import date, timedelta
DB_FILE = "postings.db"
_COLUMNS = ("company", "role", "location", "date_posted", "url", "unique_key")

def _connect():
    """Open a connection to the postings SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
def create_table():
    """Create the postings table if it does not already exist."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS postings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                role TEXT,
                location TEXT,
                date_posted TEXT,
                url TEXT,
                unique_key TEXT UNIQUE,
                date_added TEXT
            )
            """
        )
def get_existing_keys():
    """Return a set of all unique_key values currently in the table."""
    with _connect() as conn:
        rows = conn.execute("SELECT unique_key FROM postings").fetchall()
    return {row["unique_key"] for row in rows}

def insert_posting(posting):
    """Insert a posting dict as a new row, setting date_added to today."""
    values = {column: posting.get(column) for column in _COLUMNS}
    values["date_added"] = date.today().isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO postings (
                company, role, location, date_posted, url, unique_key, date_added
            ) VALUES (
                :company, :role, :location, :date_posted, :url, :unique_key, :date_added
            )
            """,
            values,
        )
def get_recent_postings(days=7):
    """Return all postings whose date_added falls within the last `days` days."""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, company, role, location, date_posted, url, unique_key, date_added
            FROM postings
            WHERE date_added >= ?
            ORDER BY date_added DESC, id DESC
            """,
            (cutoff,),
        ).fetchall()
    return [dict(row) for row in rows]
def get_all_postings():
    """Return every row in the postings table."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, company, role, location, date_posted, url, unique_key, date_added
            FROM postings
            ORDER BY id
            """
        ).fetchall()
    return [dict(row) for row in rows]