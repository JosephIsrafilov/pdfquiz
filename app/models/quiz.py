import json
import random
import secrets
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from app.database import USING_POSTGRES, db_execute, get_db_connection
from app.models.knowledge import fetch_questions_for_topics, fetch_templates_for_topics, fetch_topics_by_ids
from app.models.question_history import get_weighted_question_sample, record_question_view
from app.models.template_engine import generate_question


ALLOWED_LANGUAGES = {"en", "ru"}
ALLOWED_DIFFICULTIES = {"all", "beginner", "intermediate", "advanced"}
MAX_QUIZ_SIZE = 100


def _is_missing_submit_storage_column(error: Exception) -> bool:
    message = str(error).lower()
    error_name = type(error).__name__.lower()
    return (
        "submitted_answers_json" in message
        or "result_json" in message
        or "saved_result_id" in message
    ) and (
        "no column" in message
        or "does not exist" in message
        or "undefinedcolumn" in error_name
    )


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


def _localized_rationale(question, option, language: str) -> str:
    if not (question["option_rationales_json"] if "option_rationales_json" in question.keys() else None):
        return ""
    try:
        rationales = json.loads(question["option_rationales_json"])
        lang_rationales = rationales.get(language) or rationales.get("en") or {}
        return lang_rationales.get(option.get("text_en")) or lang_rationales.get(option.get("text_ru")) or ""
    except Exception:
        return ""



def _generate_template_instances(templates, topic_id_to_row, user_id, quiz_token, per_template=3):
    """Expand each template into a few seeded, deterministic instances.

    Seed = user identity + quiz token + template key + instance index, so the same
    student never gets the exact same numbers twice across quizzes, but re-checking
    an answer within one quiz session reproduces the identical question.
    """
    instances = []
    identity = str(user_id) if user_id is not None else "guest"
    for template in templates:
        for instance_index in range(per_template):
            seed = f"{identity}:{quiz_token}:{template['template_key']}:{instance_index}"
            generated = generate_question(dict(template), seed)
            options_text = [generated["correct"], *generated["wrong"]]
            options = [
                {"text_en": text, "text_ru": text, "is_correct": index == 0}
                for index, text in enumerate(options_text)
            ]
            topic_row = topic_id_to_row[template["topic_id"]]
            instances.append({
                "id": f"gen:{template['template_key']}:{seed}",
                "topic_id": template["topic_id"],
                "text_en": generated["text_en"],
                "text_ru": generated["text_ru"],
                "options_json": json.dumps(options, ensure_ascii=False),
                "explanation_en": "",
                "explanation_ru": "",
                "option_rationales_json": "{}",
                "difficulty": generated["difficulty"],
                "question_type": generated["question_type"],
                "topic_title_en": topic_row["title_en"],
                "topic_title_ru": topic_row["title_ru"],
                "is_generated": True,
            })
    return instances


def create_quiz(topic_ids, count: int, language: str, difficulty: str, user_id=None, room_id=None, session_exclude=None):
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
        and len(json.loads(question["options_json"])) >= 1
    ]

    quiz_token = secrets.token_urlsafe(32)
    templates = fetch_templates_for_topics(normalized_topic_ids, difficulty)
    generated_lookup = {}
    if templates:
        topic_id_to_row = {topic["id"]: topic for topic in topics}
        generated_instances = _generate_template_instances(templates, topic_id_to_row, user_id, quiz_token)
        for instance in generated_instances:
            generated_lookup[instance["id"]] = instance
        available_questions = [*available_questions, *generated_instances]

    if not available_questions:
        raise ValueError("No questions are available for this selection.")
    if count > len(available_questions):
        raise ValueError(
            f"Only {len(available_questions)} questions are available for this selection."
        )

    with get_db_connection() as connection:
        selected = get_weighted_question_sample(
            connection,
            user_id,
            available_questions,
            count,
            session_exclude=set(session_exclude) if session_exclude else None,
        )
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
            "question_type": question["question_type"] or "mcq",
            "options": [
                {"id": display_index, "text": _localized_option(options[original_index], language)}
                for display_index, original_index in enumerate(order)
            ],
        })

    random.shuffle(public_questions)
    question_ids = [question["id"] for question in public_questions]

    token = quiz_token
    with get_db_connection() as connection:
        db_execute(connection, """
            INSERT INTO quiz_sessions (
                token, user_id, language, question_order_json,
                option_orders_json, topic_ids_json, room_id, generated_questions_json
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            token,
            user_id,
            language,
            json.dumps(question_ids),
            json.dumps(option_orders),
            json.dumps(normalized_topic_ids),
            room_id,
            json.dumps({qid: generated_lookup[qid] for qid in question_ids if qid in generated_lookup}),
        ))
        connection.commit()

    topic_names = [_localized(topic, "title", language) for topic in topics]
    return {
        "token": token,
        "language": language,
        "question_count": len(public_questions),
        "topics": topic_names,
        "questions": public_questions,
        "room_id": room_id,
    }


def create_quiz_from_room(code: str, language: str, user_id=None):
    from app.models.room import fetch_room_by_code
    room = fetch_room_by_code(code)
    if not room:
        raise ValueError("Invalid or inactive room code.")
    
    topic_ids = json.loads(room["topic_ids_json"])
    count = room["question_count"] or 10
    difficulty_val = room["difficulty"] or "all"
    if difficulty_val not in ALLOWED_DIFFICULTIES:
        difficulty_val = "all"
    quiz_data = create_quiz(
        topic_ids=topic_ids,
        count=int(count),
        language=language,
        difficulty=difficulty_val,
        user_id=user_id,
        room_id=room["id"]
    )
    quiz_data["time_limit_minutes"] = room["time_limit_minutes"] if "time_limit_minutes" in room.keys() else None
    return quiz_data



def fetch_quiz_session(token: str):
    with get_db_connection() as connection:
        row = db_execute(
            connection,
            "SELECT * FROM quiz_sessions WHERE token = %s",
            (token,),
        ).fetchone()
        return dict(row) if row is not None else None


def _load_quiz_rows(quiz_session):
    question_ids = json.loads(quiz_session["question_order_json"])
    if not question_ids:
        return []

    generated_by_id = json.loads(quiz_session.get("generated_questions_json") or "{}")
    if not isinstance(generated_by_id, dict):
        # Legacy rows backfilled by the migration's DEFAULT '[]' before this
        # column was populated explicitly.
        generated_by_id = {}
    static_ids = [qid for qid in question_ids if str(qid) not in generated_by_id]

    rows_by_id = {}
    if static_ids:
        placeholders = ", ".join(["%s"] * len(static_ids))
        with get_db_connection() as connection:
            rows = db_execute(connection, f"""
                SELECT q.id, q.topic_id, q.text_en, q.text_ru, q.options_json,
                       q.explanation_en, q.explanation_ru, q.option_rationales_json, q.difficulty,
                       q.question_type,
                       t.title_en AS topic_title_en, t.title_ru AS topic_title_ru
                FROM questions q
                JOIN topics t ON t.id = q.topic_id
                WHERE q.id IN ({placeholders})
            """, tuple(static_ids)).fetchall()
        rows_by_id = {row["id"]: row for row in rows}
    for qid_str, generated in generated_by_id.items():
        rows_by_id[qid_str] = generated

    return [rows_by_id[question_id] for question_id in question_ids if question_id in rows_by_id]


def _assess_question(question, option_order, user_answer, language):
    options = json.loads(question["options_json"])
    question_type = question["question_type"] if "question_type" in question.keys() else "mcq"
    
    correct_original = {
        index for index, option in enumerate(options) if option.get("is_correct")
    }
    
    is_correct = False
    is_unanswered = False
    selected_answer = None
    
    if question_type in ("mcq", "true_false"):
        try:
            selected_display_index = int(user_answer) if user_answer is not None else None
        except (TypeError, ValueError):
            selected_display_index = None
            
        is_unanswered = selected_display_index is None
        selected_original = None
        if not is_unanswered and 0 <= selected_display_index < len(option_order):
            selected_original = option_order[selected_display_index]
            
        is_correct = selected_original in correct_original if selected_original is not None else False
        if selected_original is not None:
            selected_answer = _localized_option(options[selected_original], language)
            
        options_formatted = [
            {
                "text": _localized_option(options[original_index], language),
                "is_correct": original_index in correct_original,
                "is_selected": display_index == selected_display_index,
                "rationale": _localized_rationale(question, options[original_index], language),
            }
            for display_index, original_index in enumerate(option_order)
        ]
        
    elif question_type == "multi_select":
        if isinstance(user_answer, list):
            selected_display_indices = [int(i) for i in user_answer if str(i).isdigit()]
        elif isinstance(user_answer, str) or isinstance(user_answer, int):
            try:
                selected_display_indices = [int(user_answer)]
            except (TypeError, ValueError):
                selected_display_indices = []
        else:
            selected_display_indices = []
            
        is_unanswered = len(selected_display_indices) == 0
        
        selected_originals = set()
        for idx in selected_display_indices:
            if 0 <= idx < len(option_order):
                selected_originals.add(option_order[idx])
                
        is_correct = not is_unanswered and selected_originals == correct_original
        
        selected_answer = ", ".join(
            _localized_option(options[orig], language) for orig in selected_originals
        )
        
        options_formatted = [
            {
                "text": _localized_option(options[original_index], language),
                "is_correct": original_index in correct_original,
                "is_selected": display_index in selected_display_indices,
                "rationale": _localized_rationale(question, options[original_index], language),
            }
            for display_index, original_index in enumerate(option_order)
        ]
        
    elif question_type in ("fill_in_the_blank", "code_output"):
        user_answer_str = str(user_answer).strip() if user_answer else ""
        is_unanswered = not user_answer_str
        selected_answer = user_answer_str
        
        correct_answers_texts = [
            _localized_option(options[idx], language).strip() for idx in correct_original
        ]
        
        if not is_unanswered:
            is_correct = any(user_answer_str == t for t in correct_answers_texts)
        else:
            is_correct = False
            
        options_formatted = [
            {
                "text": _localized_option(options[original_index], language),
                "is_correct": original_index in correct_original,
                "is_selected": False,
                "rationale": _localized_rationale(question, options[original_index], language),
            }
            for display_index, original_index in enumerate(option_order)
        ]
        
    else:
        options_formatted = []

    correct_display = [
        display_index
        for display_index, original_index in enumerate(option_order)
        if original_index in correct_original
    ]
    correct_answers = [
        _localized_option(options[index], language)
        for index in sorted(correct_original)
    ]
    return {
        "question_id": question["id"],
        "question_type": question_type,
        "selected": user_answer,
        "correct_options": correct_display,
        "is_correct": is_correct,
        "is_unanswered": is_unanswered,
        "selected_answer": selected_answer,
        "correct_answers": correct_answers,
        "explanation": _localized(question, "explanation", language),
        "topic": _localized(question, "topic_title", language),
        "text": _localized(question, "text", language),
        "options": options_formatted,
    }


def check_quiz_question(token: str, question_id: int, selected, user_id=None):
    quiz_session = fetch_quiz_session(token)
    if not quiz_session:
        raise ValueError("Quiz session was not found.")
    if quiz_session["completed"]:
        raise ValueError("This quiz has already been submitted.")
    if quiz_session["user_id"] is not None and quiz_session["user_id"] != user_id:
        raise PermissionError("This quiz belongs to another user.")

    # Check if question already checked in this session
    checked = json.loads(quiz_session.get("checked_questions_json") or "[]")
    cached = next(
        (
            item.get("result")
            for item in checked
            if isinstance(item, dict) and item.get("id") == question_id
        ),
        None,
    )
    if cached is not None:
        return cached

    question_ids = json.loads(quiz_session["question_order_json"])
    if question_id not in question_ids:
        raise ValueError("Question is not part of this quiz.")
    rows = _load_quiz_rows(quiz_session)
    question = next((row for row in rows if row["id"] == question_id), None)
    if question is None:
        raise ValueError("Question is no longer available.")
    option_orders = json.loads(quiz_session["option_orders_json"])
    assessment = _assess_question(
        question,
        option_orders[str(question_id)],
        selected,
        quiz_session["language"],
    )

    # Mark question as checked and record view for logged-in users
    with get_db_connection() as connection:
        checked = json.loads(quiz_session.get("checked_questions_json") or "[]")
        if isinstance(checked, list) and question_id not in [c if isinstance(c, int) else c.get("id") for c in checked]:
            checked.append({"id": question_id, "result": assessment})
            db_execute(
                connection,
                "UPDATE quiz_sessions SET checked_questions_json = %s WHERE token = %s",
                (json.dumps(checked), token),
            )
            connection.commit()

        if user_id and isinstance(question_id, int):
            record_question_view(connection, user_id, question_id, assessment["is_correct"])

    return assessment


def submit_quiz(token: str, answers, user_id=None):
    quiz_session = fetch_quiz_session(token)
    if not quiz_session:
        raise ValueError("Quiz session was not found.")
    if quiz_session["completed"]:
        stored_result = quiz_session.get("result_json")
        if stored_result:
            result = json.loads(stored_result)
            result["_already_completed"] = True
            result["_saved_result_id"] = quiz_session.get("saved_result_id")
            return result
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
        assessment = _assess_question(
            question,
            option_orders[str(question["id"])],
            raw_selected,
            quiz_session["language"],
        )
        review.append(assessment)
        normalized_answers[str(question["id"])] = raw_selected
        if assessment["is_correct"]:
            correct += 1
        if assessment["is_unanswered"]:
            unanswered += 1
        topic = assessment["topic"]
        topic_stat = topic_stats.setdefault(topic, {"correct": 0, "total": 0})
        topic_stat["total"] += 1
        if assessment["is_correct"]:
            topic_stat["correct"] += 1

    topic_names = list(topic_stats)
    result = {
        "language": quiz_session["language"],
        "total": len(review),
        "correct": correct,
        "unanswered": unanswered,
        "score_percent": round((correct / len(review)) * 100) if review else 0,
        "topic_stats": topic_stats,
        "source_label": ", ".join(topic_names),
        "review": review,
        "answers": normalized_answers,
        "room_id": quiz_session["room_id"],
    }

    with get_db_connection() as connection:
        # Record question views for logged-in users (skip generated instances, no history row)
        if user_id:
            for question in rows:
                if "is_generated" in question.keys() and question["is_generated"]:
                    continue
                assessment = next(r for r in review if r["question_id"] == question["id"])
                record_question_view(connection, user_id, question["id"], assessment["is_correct"])

        try:
            db_execute(
                connection,
                """
                    UPDATE quiz_sessions
                    SET completed = TRUE,
                        submitted_answers_json = %s,
                        result_json = %s
                    WHERE token = %s
                """,
                (
                    json.dumps(normalized_answers),
                    json.dumps(result),
                    token,
                ),
            )
        except Exception as error:
            connection.rollback()
            if not _is_missing_submit_storage_column(error):
                raise
            db_execute(
                connection,
                "UPDATE quiz_sessions SET completed = TRUE WHERE token = %s",
                (token,),
            )
        connection.commit()

    return result


def mark_quiz_saved_result(token: str, result_id: int):
    with get_db_connection() as connection:
        try:
            db_execute(
                connection,
                "UPDATE quiz_sessions SET saved_result_id = %s WHERE token = %s",
                (result_id, token),
            )
        except Exception as error:
            connection.rollback()
            if not _is_missing_submit_storage_column(error):
                raise
            return
        connection.commit()


def cleanup_old_quiz_sessions(hours: int = 24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with get_db_connection() as connection:
        db_execute(
            connection,
            "DELETE FROM quiz_sessions WHERE created_at < %s",
            (cutoff.isoformat() if not USING_POSTGRES else cutoff,),
        )
        connection.commit()
