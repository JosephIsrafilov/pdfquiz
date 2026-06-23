import secrets
from app.database import db_execute, get_db_connection, USING_POSTGRES

def generate_group_code() -> str:
    # Generates a 6-character alphanumeric code
    return secrets.token_hex(3).upper()

def create_group(name: str, created_by: int) -> tuple[int, str]:
    code = generate_group_code()
    with get_db_connection() as connection:
        # Check for uniqueness just in case, though highly unlikely to collide often
        while True:
            existing = db_execute(connection, "SELECT id FROM groups WHERE code = %s", (code,)).fetchone()
            if not existing:
                break
            code = generate_group_code()
            
        if USING_POSTGRES:
            cursor = db_execute(
                connection,
                """
                INSERT INTO groups (name, code, created_by)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (name, code, created_by)
            )
            group_id = cursor.fetchone()["id"]
        else:
            cursor = db_execute(
                connection,
                """
                INSERT INTO groups (name, code, created_by)
                VALUES (%s, %s, %s)
                """,
                (name, code, created_by)
            )
            group_id = cursor.lastrowid
        connection.commit()
        return group_id, code

def fetch_groups_for_admin():
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT g.id, g.name, g.code, g.created_at, u.username as created_by_name,
                   (SELECT COUNT(*) FROM group_members gm WHERE gm.group_id = g.id) as member_count
            FROM groups g
            LEFT JOIN users u ON g.created_by = u.id
            ORDER BY g.created_at DESC
            """
        ).fetchall()

def join_group(code: str, user_id: int) -> tuple[bool, str]:
    with get_db_connection() as connection:
        group = db_execute(
            connection,
            "SELECT id, name FROM groups WHERE code = %s",
            (code,)
        ).fetchone()
        
        if not group:
            return False, "Group not found."
            
        group_id = group["id"] if isinstance(group, dict) else group[0]
        group_name = group["name"] if isinstance(group, dict) else group[1]
        
        # Check if already a member
        existing = db_execute(
            connection,
            "SELECT id FROM group_members WHERE group_id = %s AND user_id = %s",
            (group_id, user_id)
        ).fetchone()
        
        if existing:
            return False, "You are already a member of this group."
            
        db_execute(
            connection,
            "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
            (group_id, user_id)
        )
        connection.commit()
        return True, f"Successfully joined {group_name}!"

def fetch_user_groups(user_id: int):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT g.id, g.name, gm.joined_at, u.username as teacher_name
            FROM groups g
            JOIN group_members gm ON g.id = gm.group_id
            LEFT JOIN users u ON g.created_by = u.id
            WHERE gm.user_id = %s
            ORDER BY gm.joined_at DESC
            """,
            (user_id,)
        ).fetchall()
