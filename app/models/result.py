import json
from typing import List, Optional

from app.database import USING_POSTGRES, db_execute, get_db_connection


def _is_missing_room_id_column(error: Exception) -> bool:
    message = str(error).lower()
    error_name = type(error).__name__.lower()
    return "room_id" in message and (
        "no column" in message
        or "does not exist" in message
        or "undefinedcolumn" in error_name
    )


def fetch_results_for_user(user_id: int, limit: int = 50):
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT r.id, r.user_id, r.document_id, r.source_label,
                   r.total_questions, r.quiz_size, r.graded, r.correct,
                   r.unanswered, r.missing_answer_key,
                   r.mistake_numbers_json AS mistake_numbers,
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
                   r.unanswered, r.missing_answer_key,
                   r.mistake_numbers_json AS mistake_numbers,
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
    room_id: Optional[int] = None,
) -> Optional[int]:
    mistake_json = json.dumps(mistake_numbers)
    attempt_json = json.dumps(attempt_payload) if attempt_payload is not None else None
    returning = " RETURNING id" if USING_POSTGRES else ""
    with get_db_connection() as connection:
        try:
            cursor = db_execute(connection, f"""
                INSERT INTO results (
                    user_id, document_id, source_label, total_questions, quiz_size,
                    graded, correct, unanswered, missing_answer_key,
                    mistake_numbers_json, attempt_json, room_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s){returning}
            """, (
                user_id, document_id, source_label, total_questions, quiz_size,
                graded, correct, unanswered, missing_answer_key,
                mistake_json, attempt_json, room_id,
            ))
        except Exception as error:
            connection.rollback()
            if not _is_missing_room_id_column(error):
                raise
            cursor = db_execute(connection, f"""
                INSERT INTO results (
                    user_id, document_id, source_label, total_questions, quiz_size,
                    graded, correct, unanswered, missing_answer_key,
                    mistake_numbers_json, attempt_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s){returning}
            """, (
                user_id, document_id, source_label, total_questions, quiz_size,
                graded, correct, unanswered, missing_answer_key,
                mistake_json, attempt_json,
            ))
        connection.commit()
    if USING_POSTGRES:
        row = cursor.fetchone()
        return row[0] if row else None
    return cursor.lastrowid


def serialize_result(result):
    if result is None:
        return None
    return {
        "id": result["id"],
        "source_label": result["source_label"],
        "total_questions": result["total_questions"] or 0,
        "quiz_size": result["quiz_size"] or 0,
        "graded": result["graded"] or 0,
        "correct": result["correct"] or 0,
        "unanswered": result["unanswered"] or 0,
        "missing_answer_key": result["missing_answer_key"] or 0,
        "mistake_numbers": json.loads(result["mistake_numbers"] or "[]"),
        "created_at": str(result["created_at"]),
        "document_id": result["document_id"],
        "attempt_available": bool(result["attempt_json"]),
    }


def build_attempt_review(result):
    attempt_json = result["attempt_json"]
    if not attempt_json:
        return []
    attempt = json.loads(attempt_json)
    if isinstance(attempt, dict):
        quiz = attempt.get("quiz", [])
        answers = attempt.get("answers", {})
        attempt = []
        for index, question in enumerate(quiz):
            chosen = answers.get(str(index), answers.get(index))
            attempt.append({
                "number": question.get("number"),
                "text": question.get("text"),
                "options": question.get("options", []),
                "chosen": chosen,
            })
    review = []
    for index, item in enumerate(attempt, start=1):
        options = []
        chosen = item.get("selected", item.get("chosen"))
        for option_index, option in enumerate(item.get("options", [])):
            is_correct = bool(option.get("is_correct"))
            is_selected = bool(option.get("is_selected")) or chosen == option_index
            options.append({
                "label": chr(65 + option_index),
                "text": option.get("text", ""),
                "is_correct": is_correct,
                "is_selected": is_selected,
                "is_wrong_selected": is_selected and not is_correct,
                "rationale": option.get("rationale", ""),
            })
        review.append({
            "index": index,
            "number": item.get("number"),
            "text": item.get("text"),
            "topic": item.get("topic"),
            "explanation": item.get("explanation"),
            "selected_answer": item.get("selected_answer"),
            "correct_answers": item.get("correct_answers", []),
            "options": options,
            "chosen": chosen,
            "correct": item.get("correct_options", item.get("correct")),
            "is_correct": bool(item.get("is_correct")),
            "is_unanswered": bool(item.get("is_unanswered", chosen is None)),
        })
    return review
