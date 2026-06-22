from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db_execute, get_db_connection, get_first_column, USING_POSTGRES


def fetch_user_by_id(user_id):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT id, username, is_admin, created_at FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()


def fetch_user_by_username(username):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT id, username, password_hash, is_admin, created_at FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def serialize_user(user):
    if user is None:
        return None
    return {
        "id": user["id"],
        "username": user["username"],
        "is_admin": bool(user["is_admin"]),
        "created_at": str(user["created_at"]),
    }


def create_user(username: str, password: str):
    normalized_username = username.strip()
    with get_db_connection() as connection:
        user_count = get_first_column(
            db_execute(connection, "SELECT COUNT(*) FROM users").fetchone()
        )
        is_admin = user_count == 0
        if USING_POSTGRES:
            user = db_execute(connection, """
                INSERT INTO users (username, password_hash, is_admin)
                VALUES (%s, %s, %s)
                RETURNING id, username, is_admin, created_at
                """, (normalized_username, generate_password_hash(password), is_admin),
            ).fetchone()
            connection.commit()
            return user
        cursor = db_execute(connection, """
            INSERT INTO users (username, password_hash, is_admin)
            VALUES (%s, %s, %s)
            """, (normalized_username, generate_password_hash(password), int(is_admin)),
        )
        connection.commit()
        return db_execute(
            connection,
            "SELECT id, username, is_admin, created_at FROM users WHERE id = %s",
            (cursor.lastrowid,),
        ).fetchone()


def fetch_users():
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT id, username, is_admin, created_at FROM users ORDER BY id",
        ).fetchall()


def toggle_user_admin(user_id: int):
    with get_db_connection() as connection:
        db_execute(
            connection,
            "UPDATE users SET is_admin = NOT is_admin WHERE id = %s",
            (user_id,),
        )
        connection.commit()


def delete_user(user_id: int):
    with get_db_connection() as connection:
        db_execute(connection, "DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
