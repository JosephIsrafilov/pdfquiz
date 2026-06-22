import os
import sqlite3

try:
    import psycopg
    from psycopg.rows import dict_row
    from psycopg_pool import ConnectionPool
except ImportError:
    psycopg = None
    dict_row = None
    ConnectionPool = None

DATABASE_URL = os.environ.get("DATABASE_URL")
USING_POSTGRES = bool(DATABASE_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "app.db"))

_pool = None


def get_pool():
    global _pool
    if _pool is None and USING_POSTGRES:
        if ConnectionPool is None:
            raise RuntimeError("psycopg_pool required when DATABASE_URL is set")
        _pool = ConnectionPool(DATABASE_URL, kwargs={"row_factory": dict_row}, min_size=1, max_size=10, open=True)
    return _pool


def get_db_connection():
    if USING_POSTGRES:
        pool = get_pool()
        return pool.connection()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def db_query(query: str) -> str:
    if USING_POSTGRES:
        return query
    return query.replace("%s", "?")


def db_execute(connection, query: str, params=()):
    return connection.execute(db_query(query), params)


def get_first_column(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()))
    return row[0]


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    with get_db_connection() as connection:
        if USING_POSTGRES:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    source_label TEXT,
                    total_questions INTEGER,
                    quiz_size INTEGER,
                    graded INTEGER,
                    correct INTEGER,
                    unanswered INTEGER,
                    missing_answer_key INTEGER,
                    mistake_numbers TEXT,
                    attempt_json TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            try:
                connection.execute("ALTER TABLE results ADD COLUMN IF NOT EXISTS attempt_json TEXT")
            except Exception:
                pass
        else:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    source_label TEXT,
                    total_questions INTEGER,
                    quiz_size INTEGER,
                    graded INTEGER,
                    correct INTEGER,
                    unanswered INTEGER,
                    missing_answer_key INTEGER,
                    mistake_numbers TEXT,
                    attempt_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            try:
                connection.execute("ALTER TABLE results ADD COLUMN attempt_json TEXT")
            except Exception:
                pass
        connection.commit()
