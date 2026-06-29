import json
import secrets
import string
from app.database import db_execute, get_db_connection


def generate_room_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def create_room(title, created_by, topic_ids, difficulty, question_count, time_limit_minutes, max_attempts):
    code = generate_room_code()
    with get_db_connection() as connection:
        cursor = db_execute(connection, """
            INSERT INTO rooms (
                code, title, created_by, topic_ids_json, difficulty,
                question_count, time_limit_minutes, max_attempts
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            code, title, created_by, json.dumps(topic_ids),
            difficulty, question_count, time_limit_minutes, max_attempts
        ))
        row = cursor.fetchone()
        room_id = dict(row)["id"] if hasattr(row, "keys") else row[0]
        connection.commit()
        return room_id, code


def fetch_rooms_for_admin(admin_id=None):
    with get_db_connection() as connection:
        query = """
            SELECT r.*, u.username as creator_name
            FROM rooms r
            LEFT JOIN users u ON r.created_by = u.id
            ORDER BY r.created_at DESC
        """
        params = ()
        # If we want to restrict teachers to their own rooms in the future, we can add WHERE created_by = %s
        cursor = db_execute(connection, query, params)
        return cursor.fetchall()


def fetch_room_by_code(code):
    with get_db_connection() as connection:
        cursor = db_execute(connection, """
            SELECT * FROM rooms WHERE code = %s AND is_active = TRUE
        """, (code,))
        return cursor.fetchone()


def fetch_room_by_id(room_id):
    with get_db_connection() as connection:
        cursor = db_execute(connection, """
            SELECT * FROM rooms WHERE id = %s
        """, (room_id,))
        return cursor.fetchone()


def toggle_room_active(room_id):
    with get_db_connection() as connection:
        db_execute(connection, """
            UPDATE rooms SET is_active = NOT is_active WHERE id = %s
        """, (room_id,))
        connection.commit()


def fetch_room_results(room_id, group_id=None):
    with get_db_connection() as connection:
        if group_id:
            query = """
                SELECT r.*, u.username 
                FROM results r
                LEFT JOIN users u ON r.user_id = u.id
                JOIN group_members gm ON u.id = gm.user_id
                WHERE r.room_id = %s AND gm.group_id = %s
                ORDER BY r.created_at DESC
            """
            params = (room_id, group_id)
        else:
            query = """
                SELECT r.*, u.username 
                FROM results r
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.room_id = %s
                ORDER BY r.created_at DESC
            """
            params = (room_id,)
        cursor = db_execute(connection, query, params)
        return cursor.fetchall()


def analyze_room_questions(results):
    question_stats = {}
    for r in results:
        attempt_json = r.get("attempt_json") if hasattr(r, "get") else r["attempt_json"]
        if not attempt_json:
            continue
        try:
            attempt = json.loads(attempt_json) if isinstance(attempt_json, str) else attempt_json
            if isinstance(attempt, dict):
                quiz = attempt.get("quiz", [])
                answers = attempt.get("answers", {})
                for idx, question in enumerate(quiz):
                    qid = question.get("id")
                    if not qid:
                        continue
                    if qid not in question_stats:
                        question_stats[qid] = {
                            "id": qid,
                            "text": question.get("text", ""),
                            "total_attempts": 0,
                            "correct_attempts": 0
                        }
                    
                    # Check correctness
                    selected = answers.get(str(idx))
                    if selected is None:
                        selected = answers.get(idx)
                        
                    is_correct = False
                    if question.get("question_type") == "multi_select":
                        # For multi_select, options are a list of selected indices
                        if selected is not None:
                            correct_indices = {i for i, opt in enumerate(question.get("options", [])) if opt.get("is_correct")}
                            is_correct = set(selected) == correct_indices
                    elif question.get("question_type") in ("fill_in_the_blank", "code_output"):
                        if selected:
                            correct_opts = [opt.get("text", "").strip().lower() for opt in question.get("options", []) if opt.get("is_correct")]
                            is_correct = str(selected).strip().lower() in correct_opts
                    else:
                        if selected is not None:
                            is_correct = question["options"][int(selected)].get("is_correct", False)
                    
                    question_stats[qid]["total_attempts"] += 1
                    if is_correct:
                        question_stats[qid]["correct_attempts"] += 1
            elif isinstance(attempt, list):
                for item in attempt:
                    qid = item.get("question_id")
                    if not qid:
                        continue
                    if qid not in question_stats:
                        question_stats[qid] = {
                            "id": qid,
                            "text": item.get("question_text", ""),
                            "total_attempts": 0,
                            "correct_attempts": 0
                        }
                    question_stats[qid]["total_attempts"] += 1
                    if item.get("is_correct"):
                        question_stats[qid]["correct_attempts"] += 1
        except Exception:
            continue
            
    for stats in question_stats.values():
        if stats["total_attempts"] > 0:
            stats["accuracy"] = (stats["correct_attempts"] / stats["total_attempts"]) * 100
        else:
            stats["accuracy"] = 0
            
    # Sort by accuracy (lowest first)
    return sorted(list(question_stats.values()), key=lambda x: x["accuracy"])
