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
        _pool = ConnectionPool(
            DATABASE_URL,
            kwargs={"row_factory": dict_row, "prepare_threshold": None},
            min_size=1,
            max_size=10,
            max_idle=300,
            check=ConnectionPool.check_connection,
            open=True,
        )
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
        connection.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)")
        connection.commit()
        
        if USING_POSTGRES:
            applied = [r['version'] for r in connection.execute("SELECT version FROM schema_migrations").fetchall()]
        else:
            applied = [r[0] for r in connection.execute("SELECT version FROM schema_migrations").fetchall()]
            
        migrations_dir = os.path.join(BASE_DIR, "migrations")
        if not os.path.exists(migrations_dir):
            return
            
        import importlib.util
        
        for filename in sorted(os.listdir(migrations_dir)):
            if filename.endswith(".py"):
                version_str = filename.split("_")[0]
                try:
                    version = int(version_str)
                except ValueError:
                    continue
                    
                if version not in applied:
                    mod_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(migrations_dir, filename))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    mod.upgrade(connection, USING_POSTGRES)
                    
                    if USING_POSTGRES:
                        connection.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (version,))
                    else:
                        connection.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))
                    connection.commit()
