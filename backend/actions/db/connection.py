# actions/db/connection.py

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Try to use PostgreSQL if psycopg2 is available and required env vars are set.
USE_POSTGRES = False
db_pool = None

try:
    import psycopg2
    from psycopg2 import pool

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    if POSTGRES_HOST and POSTGRES_DB and POSTGRES_USER:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
            )
            USE_POSTGRES = True
            print("✅ PostgreSQL connection pool created successfully.")
        except Exception as e:
            print("❌ ERROR: Could not create PostgreSQL connection pool.")
            print(e)
    else:
        print("ℹ️ PostgreSQL env vars not fully set; falling back to SQLite.")
except Exception:
    print("ℹ️ psycopg2 not available; falling back to SQLite.")


# -----------------------------
# SQLITE FALLBACK
# -----------------------------
SQLITE_DB_PATH = Path(__file__).parent / "database.sqlite3"
SCHEMA_FILE = Path(__file__).parent / "schema.sql"

def _ensure_sqlite_db():
    if not SQLITE_DB_PATH.exists():
        print(f"ℹ️ Creating SQLite DB at {SQLITE_DB_PATH}")
        conn = sqlite3.connect(SQLITE_DB_PATH)
        try:
            if SCHEMA_FILE.exists():
                with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
            conn.commit()
        finally:
            conn.close()


def get_conn():
    """Return a DB connection. Uses Postgres pool when available, otherwise SQLite."""
    if USE_POSTGRES and db_pool is not None:
        try:
            return db_pool.getconn()
        except Exception as e:
            print("❌ ERROR: Unable to get Postgres DB connection:", e)
            return None

    # Ensure SQLite DB exists and return a sqlite3.Connection with row access by name
    try:
        _ensure_sqlite_db()
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print("❌ ERROR: Unable to get SQLite DB connection:", e)
        return None


def release_conn(conn):
    """Release/close a connection depending on the backend used."""
    if conn is None:
        return

    if USE_POSTGRES and db_pool is not None:
        try:
            db_pool.putconn(conn)
        except Exception as e:
            print("❌ ERROR releasing Postgres connection:", e)
    else:
        try:
            conn.close()
        except Exception as e:
            print("❌ ERROR closing SQLite connection:", e)