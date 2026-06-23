import json
from typing import Iterable, Optional

from app.database import USING_POSTGRES, db_execute, get_db_connection


def _insert_and_get_id(connection, query: str, params) -> int:
    if USING_POSTGRES:
        row = db_execute(connection, f"{query} RETURNING id", params).fetchone()
        return row["id"]
    cursor = db_execute(connection, query, params)
    return cursor.lastrowid


def fetch_catalog(active_only: bool = True):
    active_filter = "WHERE c.is_active = TRUE" if active_only else ""
    topic_active_filter = "AND t.is_active = TRUE" if active_only else ""
    question_active_filter = "AND q.is_active = TRUE" if active_only else ""
    with get_db_connection() as connection:
        courses = db_execute(connection, f"""
            SELECT c.id, c.title_en, c.title_ru, c.is_active,
                   COUNT(DISTINCT CASE WHEN t.is_active = TRUE THEN t.id END) AS topic_count,
                   COUNT(DISTINCT CASE WHEN q.is_active = TRUE THEN q.id END) AS question_count
            FROM courses c
            LEFT JOIN topics t ON t.course_id = c.id {topic_active_filter}
            LEFT JOIN questions q ON q.topic_id = t.id {question_active_filter}
            {active_filter}
            GROUP BY c.id, c.title_en, c.title_ru, c.is_active
            ORDER BY c.id
        """).fetchall()
        topics = db_execute(connection, f"""
            SELECT t.id, t.course_id, t.title_en, t.title_ru,
                   t.description_en, t.description_ru, t.sort_order, t.is_active,
                   COUNT(q.id) AS question_count,
                   SUM(CASE WHEN q.difficulty = 'beginner' THEN 1 ELSE 0 END) AS beginner_count,
                   SUM(CASE WHEN q.difficulty = 'intermediate' THEN 1 ELSE 0 END) AS intermediate_count,
                   SUM(CASE WHEN q.difficulty = 'advanced' THEN 1 ELSE 0 END) AS advanced_count
            FROM topics t
            LEFT JOIN questions q ON q.topic_id = t.id {question_active_filter}
            {"WHERE t.is_active = TRUE" if active_only else ""}
            GROUP BY t.id, t.course_id, t.title_en, t.title_ru,
                     t.description_en, t.description_ru, t.sort_order, t.is_active
            ORDER BY t.course_id, t.sort_order, t.id
        """).fetchall()

    topics_by_course = {}
    for row in topics:
        topics_by_course.setdefault(row["course_id"], []).append(dict(row))
    result = []
    for row in courses:
        course = dict(row)
        course["is_active"] = bool(course["is_active"])
        course["topics"] = topics_by_course.get(course["id"], [])
        for topic in course["topics"]:
            topic["is_active"] = bool(topic["is_active"])
        result.append(course)
    return result


def fetch_topics_by_ids(topic_ids: Iterable[int], active_only: bool = True):
    ids = list(dict.fromkeys(int(value) for value in topic_ids))
    if not ids:
        return []
    placeholders = ", ".join(["%s"] * len(ids))
    active_filter = "AND t.is_active = TRUE AND c.is_active = TRUE" if active_only else ""
    with get_db_connection() as connection:
        return db_execute(connection, f"""
            SELECT t.id, t.course_id, t.title_en, t.title_ru,
                   c.title_en AS course_title_en, c.title_ru AS course_title_ru
            FROM topics t
            JOIN courses c ON c.id = t.course_id
            WHERE t.id IN ({placeholders}) {active_filter}
            ORDER BY t.sort_order, t.id
        """, tuple(ids)).fetchall()


def fetch_questions_for_topics(
    topic_ids: Iterable[int],
    difficulty: Optional[str] = None,
    active_only: bool = True,
):
    ids = list(dict.fromkeys(int(value) for value in topic_ids))
    if not ids:
        return []
    placeholders = ", ".join(["%s"] * len(ids))
    conditions = [f"q.topic_id IN ({placeholders})"]
    params = list(ids)
    if active_only:
        conditions.append("q.is_active = TRUE")
        conditions.append("t.is_active = TRUE")
        conditions.append("c.is_active = TRUE")
    if difficulty and difficulty != "all":
        conditions.append("q.difficulty = %s")
        params.append(difficulty)
    with get_db_connection() as connection:
        return db_execute(connection, f"""
            SELECT q.id, q.topic_id, q.text_en, q.text_ru, q.options_json,
                   q.explanation_en, q.explanation_ru, q.difficulty, q.is_active,
                   t.title_en AS topic_title_en, t.title_ru AS topic_title_ru,
                   c.title_en AS course_title_en, c.title_ru AS course_title_ru
            FROM questions q
            JOIN topics t ON t.id = q.topic_id
            JOIN courses c ON c.id = t.course_id
            WHERE {" AND ".join(conditions)}
            ORDER BY q.id
        """, tuple(params)).fetchall()


def fetch_question(question_id: int):
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT q.id, q.topic_id, q.text_en, q.text_ru, q.options_json,
                   q.explanation_en, q.explanation_ru, q.difficulty, q.is_active,
                   t.title_en AS topic_title_en, t.title_ru AS topic_title_ru
            FROM questions q
            JOIN topics t ON t.id = q.topic_id
            WHERE q.id = %s
        """, (question_id,)).fetchone()


def fetch_questions_for_admin():
    with get_db_connection() as connection:
        return db_execute(connection, """
            SELECT q.id, q.topic_id, q.text_en, q.text_ru, q.options_json,
                   q.explanation_en, q.explanation_ru, q.difficulty, q.is_active,
                   t.title_en AS topic_title_en, t.title_ru AS topic_title_ru,
                   c.title_en AS course_title_en, c.title_ru AS course_title_ru
            FROM questions q
            JOIN topics t ON t.id = q.topic_id
            JOIN courses c ON c.id = t.course_id
            ORDER BY c.id, t.sort_order, q.id DESC
        """).fetchall()


def create_course(title_en: str, title_ru: str):
    with get_db_connection() as connection:
        course_id = _insert_and_get_id(
            connection,
            "INSERT INTO courses (title_en, title_ru) VALUES (%s, %s)",
            (title_en.strip(), title_ru.strip()),
        )
        connection.commit()
        return course_id


def create_topic(
    course_id: int,
    title_en: str,
    title_ru: str,
    description_en: str = "",
    description_ru: str = "",
    sort_order: int = 0,
):
    with get_db_connection() as connection:
        topic_id = _insert_and_get_id(
            connection,
            """
            INSERT INTO topics (
                course_id, title_en, title_ru, description_en, description_ru, sort_order
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                course_id,
                title_en.strip(),
                title_ru.strip(),
                description_en.strip(),
                description_ru.strip(),
                sort_order,
            ),
        )
        connection.commit()
        return topic_id


def create_question(
    topic_id: int,
    text_en: str,
    text_ru: str,
    options,
    explanation_en: str = "",
    explanation_ru: str = "",
    difficulty: str = "beginner",
):
    with get_db_connection() as connection:
        question_id = _insert_and_get_id(
            connection,
            """
            INSERT INTO questions (
                topic_id, text_en, text_ru, options_json,
                explanation_en, explanation_ru, difficulty
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                topic_id,
                text_en.strip(),
                text_ru.strip(),
                json.dumps(options, ensure_ascii=False),
                explanation_en.strip(),
                explanation_ru.strip(),
                difficulty,
            ),
        )
        connection.commit()
        return question_id


def update_question(
    question_id: int,
    topic_id: int,
    text_en: str,
    text_ru: str,
    options,
    explanation_en: str,
    explanation_ru: str,
    difficulty: str,
):
    with get_db_connection() as connection:
        db_execute(connection, """
            UPDATE questions
            SET topic_id = %s, text_en = %s, text_ru = %s, options_json = %s,
                explanation_en = %s, explanation_ru = %s, difficulty = %s
            WHERE id = %s
        """, (
            topic_id,
            text_en.strip(),
            text_ru.strip(),
            json.dumps(options, ensure_ascii=False),
            explanation_en.strip(),
            explanation_ru.strip(),
            difficulty,
            question_id,
        ))
        connection.commit()


def toggle_question(question_id: int):
    with get_db_connection() as connection:
        db_execute(
            connection,
            "UPDATE questions SET is_active = NOT is_active WHERE id = %s",
            (question_id,),
        )
        connection.commit()


def delete_question(question_id: int):
    with get_db_connection() as connection:
        db_execute(connection, "DELETE FROM questions WHERE id = %s", (question_id,))
        connection.commit()


def _translated_option(text: str) -> str:
    from app.curriculum.python_core import OPTION_TRANSLATIONS_RU

    return OPTION_TRANSLATIONS_RU.get(text, text)


def _teaching_explanation(topic, question, language: str) -> str:
    correct_en = question["correct"]
    correct_ru = _translated_option(correct_en)
    wrong_en = question["wrong"][:2]
    wrong_ru = [_translated_option(value) for value in wrong_en]
    level_en = {
        "beginner": "Connect the keyword or value to its basic purpose.",
        "intermediate": "Trace the code or rule one step at a time before choosing.",
        "advanced": "Pay attention to exact Python behavior, evaluation order, and edge cases.",
    }[question["difficulty"]]
    level_ru = {
        "beginner": "Свяжите ключевое слово или значение с его основным назначением.",
        "intermediate": "Перед выбором проследите выполнение кода или правила по шагам.",
        "advanced": "Обратите внимание на точное поведение Python, порядок вычислений и граничные случаи.",
    }[question["difficulty"]]
    if language == "ru":
        return "\n".join([
            f"Понятие: {topic['description_ru']}",
            f"Почему это верно: правильный ответ — «{correct_ru}». Он точно соответствует тому, о чём спрашивает вопрос.",
            f"Как рассуждать: {level_ru}",
            f"Частая ошибка: варианты «{wrong_ru[0]}» и «{wrong_ru[1]}» относятся к другому синтаксису или поведению и не выполняют условие вопроса.",
            "Закрепление: попробуйте своими словами объяснить правило, а затем измените пример и предскажите результат до запуска кода.",
        ])
    return "\n".join([
        f"Concept: {topic['description_en']}",
        f"Why it is correct: the correct answer is “{correct_en}”. It directly matches the behavior or rule asked about.",
        f"How to reason: {level_en}",
        f"Common trap: “{wrong_en[0]}” and “{wrong_en[1]}” describe different syntax or behavior, so they do not satisfy this question.",
        "Practice idea: explain the rule in your own words, then change the example and predict the result before running it.",
    ])


def synchronize_python_curriculum():
    from app.curriculum.python_core import (
        COURSE_TITLE_EN,
        COURSE_TITLE_RU,
        PYTHON_TOPICS,
    )
    from app.curriculum.python_deep import PYTHON_DEEP_TOPICS

    curriculum_topics = [*PYTHON_TOPICS, *PYTHON_DEEP_TOPICS]

    with get_db_connection() as connection:
        course = db_execute(
            connection,
            "SELECT id FROM courses WHERE title_en = %s ORDER BY id LIMIT 1",
            (COURSE_TITLE_EN,),
        ).fetchone()
        if course:
            course_id = course["id"]
        else:
            course_id = _insert_and_get_id(
                connection,
                "INSERT INTO courses (title_en, title_ru) VALUES (%s, %s)",
                (COURSE_TITLE_EN, COURSE_TITLE_RU),
            )

        for sort_order, topic in enumerate(curriculum_topics, start=1):
            topic_key = f"python-core:{topic['key']}"
            row = db_execute(
                connection,
                "SELECT id FROM topics WHERE curriculum_key = %s",
                (topic_key,),
            ).fetchone()
            if row:
                topic_id = row["id"]
                db_execute(connection, """
                    UPDATE topics
                    SET title_en = %s, title_ru = %s, description_en = %s,
                        description_ru = %s, sort_order = %s
                    WHERE id = %s
                """, (
                    topic["title_en"],
                    topic["title_ru"],
                    topic["description_en"],
                    topic["description_ru"],
                    sort_order,
                    topic_id,
                ))
            else:
                topic_id = _insert_and_get_id(connection, """
                    INSERT INTO topics (
                        course_id, title_en, title_ru, description_en,
                        description_ru, sort_order, curriculum_key
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    course_id,
                    topic["title_en"],
                    topic["title_ru"],
                    topic["description_en"],
                    topic["description_ru"],
                    sort_order,
                    topic_key,
                ))

            for question_index, question in enumerate(topic["questions"], start=1):
                question_key = f"{topic_key}:q{question_index}"
                options_text = [question["correct"], *question["wrong"]]
                options = [
                    {
                        "text_en": text,
                        "text_ru": _translated_option(text),
                        "is_correct": index == 0,
                    }
                    for index, text in enumerate(options_text)
                ]
                explanation_en = (
                    question.get("explanation_en")
                    or _teaching_explanation(topic, question, "en")
                )
                explanation_ru = (
                    question.get("explanation_ru")
                    or _teaching_explanation(topic, question, "ru")
                )
                existing_question = db_execute(
                    connection,
                    "SELECT id FROM questions WHERE curriculum_key = %s",
                    (question_key,),
                ).fetchone()
                values = (
                    topic_id,
                    question["text_en"],
                    question["text_ru"],
                    json.dumps(options, ensure_ascii=False),
                    explanation_en,
                    explanation_ru,
                    question["difficulty"],
                )
                if existing_question:
                    db_execute(connection, """
                        UPDATE questions
                        SET topic_id = %s, text_en = %s, text_ru = %s,
                            options_json = %s, explanation_en = %s,
                            explanation_ru = %s, difficulty = %s
                        WHERE id = %s
                    """, (*values, existing_question["id"]))
                else:
                    db_execute(connection, """
                        INSERT INTO questions (
                            topic_id, text_en, text_ru, options_json,
                            explanation_en, explanation_ru, difficulty, curriculum_key
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (*values, question_key))
        connection.commit()
