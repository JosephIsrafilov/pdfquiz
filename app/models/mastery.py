from datetime import datetime
from app.database import db_execute, get_db_connection


def update_mastery_after_quiz(user_id: int, results: list):
    """
    Update mastery after quiz submission.
    results: list of dicts with topic_id, difficulty, was_correct
    """
    if not user_id:
        return

    with get_db_connection() as connection:
        for result in results:
            topic_id = result["topic_id"]
            difficulty = result["difficulty"]
            was_correct = result["was_correct"]

            existing = db_execute(connection, """
                SELECT id, total_attempts, correct_attempts, mastery_score
                FROM user_topic_mastery
                WHERE user_id = %s AND topic_id = %s AND difficulty = %s
            """, (user_id, topic_id, difficulty)).fetchone()

            if existing:
                total = existing["total_attempts"] + 1
                correct = existing["correct_attempts"] + (1 if was_correct else 0)
                mastery = correct / total if total > 0 else 0.0
                locked = mastery >= 0.9 and total >= 2

                db_execute(connection, """
                    UPDATE user_topic_mastery
                    SET total_attempts = %s, correct_attempts = %s, mastery_score = %s,
                        locked = %s, last_attempt_at = %s
                    WHERE id = %s
                """, (total, correct, mastery, locked, datetime.now(), existing["id"]))
            else:
                correct = 1 if was_correct else 0
                mastery = correct / 1
                locked = mastery >= 0.9 and 1 >= 2

                db_execute(connection, """
                    INSERT INTO user_topic_mastery (
                        user_id, topic_id, difficulty, total_attempts, correct_attempts,
                        mastery_score, locked, last_attempt_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, topic_id, difficulty, 1, correct, mastery, locked, datetime.now()))

        connection.commit()


def get_allowed_difficulties(user_id: int, topic_id: int) -> list:
    """
    Return list of unlocked difficulties for topic.
    If beginner locked → ["intermediate", "advanced"]
    """
    if not user_id:
        return ["beginner", "intermediate", "advanced"]

    with get_db_connection() as connection:
        locked = db_execute(connection, """
            SELECT difficulty FROM user_topic_mastery
            WHERE user_id = %s AND topic_id = %s AND locked = TRUE
        """, (user_id, topic_id)).fetchall()

        locked_set = {row["difficulty"] for row in locked}

    all_diffs = ["beginner", "intermediate", "advanced"]
    return [d for d in all_diffs if d not in locked_set]


def get_mastery_status(user_id: int) -> dict:
    """
    Return mastery status for all topics.
    Format: {topic_id: {difficulty: {mastery_score, locked}}}
    """
    if not user_id:
        return {}

    with get_db_connection() as connection:
        rows = db_execute(connection, """
            SELECT topic_id, difficulty, mastery_score, locked
            FROM user_topic_mastery
            WHERE user_id = %s
        """, (user_id,)).fetchall()

    result = {}
    for row in rows:
        tid = row["topic_id"]
        if tid not in result:
            result[tid] = {}
        result[tid][row["difficulty"]] = {
            "mastery_score": row["mastery_score"],
            "locked": bool(row["locked"]),
        }

    return result
