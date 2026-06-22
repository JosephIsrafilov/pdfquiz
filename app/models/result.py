import json
from typing import List, Optional

from app.database import db_execute, get_db_connection


def fetch_results_for_user(user_id: int, limit: int = 50):
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT r.id, r.user_id, r.document_id, r.source_label,
                   r.total_questions, r.quiz_size, r.graded, r.correct,
                   r.unanswered, r.missing_answer_key, r.mistake_numbers,
                   r.attempt_json, r.created_at, d.title AS document_title
            FROM results r
            LEFT JOIN documents d ON r.document_id = d.id
            WHERE r.user_id = %s
            ORDER BY r.id DESC
            LIMIT %s
        """, (user_id, limit)).fetchall()


def fetch_result_for_user(result_id: int, user_id: int):
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT r.id, r.user_id, r.document_id, r.source_label,
                   r.total_questions, r.quiz_size, r.graded, r.correct,
                   r.unanswered, r.missing_answer_key, r.mistake_numbers,
                   r.attempt_json, r.created_at, d.title AS document_title
            FROM results r
            LEFT JOIN documents d ON r.document_id = d.id
            WHERE r.id = %s AND r.user_id = %s
        """, (result_id, user_id)).fetchone()


def save_result(
    user_id: int,
    document_id: Optional[int],
    source_label: str,
    total_questions: int,
    quiz_size: int,
    graded: int,
    correct: int,
    unanswered: int,
    missing_answer_key: int,
    mistake_numbers: List[int],
    attempt_payload,
):
    mistake_json = json.dumps(mistake_numbers)
    attempt_json = json.dumps(attempt_payload) if attempt_payload is not None else None
    with get_db_connection() as connection:
        db_execute(connection, """
            INSERT INTO results (
                user_id, document_id, source_label, total_questions, quiz_size,
                graded, correct, unanswered, missing_answer_key,
                mistake_numbers, attempt_json
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, document_id, source_label, total_questions, quiz_size,
            graded, correct, unanswered, missing_answer_key,
            mistake_json, attempt_json,
        ))
        connection.commit()


def serialize_result(result):
    if result is None:
        return None
    return {
        "id": result["id"],
        "source_label": result["source_label"],
        "total_questions": result["total_questions"],
        "quiz_size": result["quiz_size"],
        "graded": result["graded"],
        "correct": result["correct"],
        "unanswered": result["unanswered"],
        "missing_answer_key": result["missing_answer_key"],
        "mistake_numbers": json.loads(result["mistake_numbers"] or "[]"),
        "created_at": str(result["created_at"]),
        "document_id": result["document_id"],
    }


def build_attempt_review(result):
    attempt_json = result["attempt_json"]
    if not attempt_json:
        return []
    attempt = json.loads(attempt_json)
    review = []
    for item in attempt:
        review.append({
            "number": item.get("number"),
            "text": item.get("text"),
            "options": item.get("options", []),
            "chosen": item.get("chosen"),
            "correct": item.get("correct"),
            "is_correct": item.get("is_correct"),
        })
    return review
