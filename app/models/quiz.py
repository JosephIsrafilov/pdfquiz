import json
import random
import secrets
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from app.database import USING_POSTGRES, db_execute, get_db_connection
from app.models.knowledge import fetch_questions_for_topics, fetch_topics_by_ids


ALLOWED_LANGUAGES = {"en", "ru"}
ALLOWED_DIFFICULTIES = {"all", "beginner", "intermediate", "advanced"}
MAX_QUIZ_SIZE = 100


def _localized(row, field: str, language: str) -> str:
    primary = row[f"{field}_{language}"]
    fallback = row[f"{field}_{'ru' if language == 'en' else 'en'}"]
    return (primary or fallback or "").strip()


def _localized_option(option, language: str) -> str:
    return (
        option.get(f"text_{language}")
        or option.get(f"text_{'ru' if language == 'en' else 'en'}")
        or option.get("text")
        or ""
    ).strip()


def _balanced_sample(questions, topic_ids, count):
    by_topic = defaultdict(list)
    for question in questions:
        by_topic[question["topic_id"]].append(question)
    for pool in by_topic.values():
        random.shuffle(pool)

    selected = []
    active_topics = [topic_id for topic_id in topic_ids if by_topic[topic_id]]
    while len(selected) < count and active_topics:
        next_round = []
        for topic_id in active_topics:
            if len(selected) >= count:
                break
            if by_topic[topic_id]:
                selected.append(by_topic[topic_id].pop())
            if by_topic[topic_id]:
                next_round.append(topic_id)
        active_topics = next_round
    random.shuffle(selected)
    return selected


def create_quiz(topic_ids, count: int, language: str, difficulty: str, user_id=None):
    if language not in ALLOWED_LANGUAGES:
        raise ValueError("Unsupported language.")
    if difficulty not in ALLOWED_DIFFICULTIES:
        raise ValueError("Unsupported difficulty.")
    if count < 1 or count > MAX_QUIZ_SIZE:
        raise ValueError(f"Question count must be between 1 and {MAX_QUIZ_SIZE}.")

    normalized_topic_ids = list(dict.fromkeys(int(value) for value in topic_ids))
    topics = fetch_topics_by_ids(normalized_topic_ids)
    if len(topics) != len(normalized_topic_ids):
        raise ValueError("One or more selected topics are unavailable.")

    questions = fetch_questions_for_topics(normalized_topic_ids, difficulty)
    available_questions = [
        question
        for question in questions
        if _localized(question, "text", language)
        and len(json.loads(question["options_json"])) >= 2
    ]
    if not available_questions:
        raise ValueError("No questions are available for this selection.")
    if count > len(available_questions):
        raise ValueError(
            f"Only {len(available_questions)} questions are available for this selection."
        )

    selected = _balanced_sample(
        available_questions,
        normalized_topic_ids,
        count,
    )
    question_ids = [question["id"] for question in selected]
    option_orders = {}
    public_questions = []
    for question in selected:
        options = json.loads(question["options_json"])
        order = list(range(len(options)))
        random.shuffle(order)
        option_orders[str(question["id"])] = order
        public_questions.append({
            "id": question["id"],
            "text": _localized(question, "text", language),
            "topic": _localized(question, "topic_title", language),
            "difficulty": question["difficulty"],
            "options": [
                {"id": display_index, "text": _localized_option(options[original_index], language)}
                for display_index, original_index in enumerate(order)
            ],
        })

    token = secrets.token_urlsafe(32)
    with get_db_connection() as connection:
        db_execute(connection, """
            INSERT INTO quiz_sessions (
                token, user_id, language, question_order_json,
                option_orders_json, topic_ids_json
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            token,
            user_id,
            language,
            json.dumps(question_ids),
            json.dumps(option_orders),
            json.dumps(normalized_topic_ids),
        ))
        connection.commit()

    topic_names = [_localized(topic, "title", language) for topic in topics]
    return {
        "token": token,
        "language": language,
        "question_count": len(public_questions),
        "topics": topic_names,
        "questions": public_questions,
    }


def fetch_quiz_session(token: str):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT * FROM quiz_sessions WHERE token = %s",
            (token,),
        ).fetchone()


def _load_quiz_rows(quiz_session):
    question_ids = json.loads(quiz_session["question_order_json"])
    if not question_ids:
        return []
    placeholders = ", ".join(["%s"] * len(question_ids))
    with get_db_connection() as connection:
        rows = db_execute(connection, f"""
            SELECT q.id, q.topic_id, q.text_en, q.text_ru, q.options_json,
                   q.explanation_en, q.explanation_ru, q.difficulty,
                   t.title_en AS topic_title_en, t.title_ru AS topic_title_ru
            FROM questions q
            JOIN topics t ON t.id = q.topic_id
            WHERE q.id IN ({placeholders})
        """, tuple(question_ids)).fetchall()
    rows_by_id = {row["id"]: row for row in rows}
    return [rows_by_id[question_id] for question_id in question_ids if question_id in rows_by_id]


def _assess_question(question, option_order, selected_display_index, language):
    options = json.loads(question["options_json"])
    correct_original = {
        index for index, option in enumerate(options) if option.get("is_correct")
    }
    selected_original = None
    if isinstance(selected_display_index, int) and 0 <= selected_display_index < len(option_order):
        selected_original = option_order[selected_display_index]
    correct_display = [
        display_index
        for display_index, original_index in enumerate(option_order)
        if original_index in correct_original
    ]
    selected_answer = None
    if selected_original is not None:
        selected_answer = _localized_option(options[selected_original], language)
    correct_answers = [
        _localized_option(options[index], language)
        for index in sorted(correct_original)
    ]
    return {
        "question_id": question["id"],
        "selected": selected_display_index,
        "correct_options": correct_display,
        "is_correct": selected_original in correct_original if selected_original is not None else False,
        "is_unanswered": selected_original is None,
        "selected_answer": selected_answer,
        "correct_answers": correct_answers,
        "explanation": _localized(question, "explanation", language),
        "topic": _localized(question, "topic_title", language),
        "text": _localized(question, "text", language),
        "options": [
            {
                "text": _localized_option(options[original_index], language),
                "is_correct": original_index in correct_original,
                "is_selected": display_index == selected_display_index,
            }
            for display_index, original_index in enumerate(option_order)
        ],
    }


def check_quiz_question(token: str, question_id: int, selected, user_id=None):
    quiz_session = fetch_quiz_session(token)
    if not quiz_session:
        raise ValueError("Quiz session was not found.")
    if quiz_session["completed"]:
        raise ValueError("This quiz has already been submitted.")
    if quiz_session["user_id"] is not None and quiz_session["user_id"] != user_id:
        raise PermissionError("This quiz belongs to another user.")

    question_ids = json.loads(quiz_session["question_order_json"])
    if question_id not in question_ids:
        raise ValueError("Question is not part of this quiz.")
    rows = _load_quiz_rows(quiz_session)
    question = next((row for row in rows if row["id"] == question_id), None)
    if question is None:
        raise ValueError("Question is no longer available.")
    option_orders = json.loads(quiz_session["option_orders_json"])
    return _assess_question(
        question,
        option_orders[str(question_id)],
        selected,
        quiz_session["language"],
    )


def submit_quiz(token: str, answers, user_id=None):
    quiz_session = fetch_quiz_session(token)
    if not quiz_session:
        raise ValueError("Quiz session was not found.")
    if quiz_session["completed"]:
        raise ValueError("This quiz has already been submitted.")
    if quiz_session["user_id"] is not None and quiz_session["user_id"] != user_id:
        raise PermissionError("This quiz belongs to another user.")

    option_orders = json.loads(quiz_session["option_orders_json"])
    rows = _load_quiz_rows(quiz_session)
    review = []
    topic_stats = {}
    correct = 0
    unanswered = 0
    normalized_answers = {}
    for question in rows:
        raw_selected = answers.get(str(question["id"]), answers.get(question["id"]))
        try:
            selected = int(raw_selected) if raw_selected is not None else None
        except (TypeError, ValueError):
            selected = None
        assessment = _assess_question(
            question,
            option_orders[str(question["id"])],
            selected,
            quiz_session["language"],
        )
        review.append(assessment)
        normalized_answers[str(question["id"])] = selected
        if assessment["is_correct"]:
            correct += 1
        if assessment["is_unanswered"]:
            unanswered += 1
        topic = assessment["topic"]
        topic_stat = topic_stats.setdefault(topic, {"correct": 0, "total": 0})
        topic_stat["total"] += 1
        if assessment["is_correct"]:
            topic_stat["correct"] += 1

    with get_db_connection() as connection:
        db_execute(
            connection,
            "UPDATE quiz_sessions SET completed = TRUE WHERE token = %s",
            (token,),
        )
        connection.commit()

    topic_names = list(topic_stats)
    return {
        "language": quiz_session["language"],
        "total": len(review),
        "correct": correct,
        "unanswered": unanswered,
        "score_percent": round((correct / len(review)) * 100) if review else 0,
        "topic_stats": topic_stats,
        "source_label": ", ".join(topic_names),
        "review": review,
        "answers": normalized_answers,
    }


def cleanup_old_quiz_sessions(hours: int = 24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with get_db_connection() as connection:
        db_execute(
            connection,
            "DELETE FROM quiz_sessions WHERE created_at < %s",
            (cutoff.isoformat() if not USING_POSTGRES else cutoff,),
        )
        connection.commit()
