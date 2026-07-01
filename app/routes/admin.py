import json
from zipfile import BadZipFile

from flask import redirect, render_template, request, session, url_for

from app.models.knowledge import (
    create_course,
    create_question,
    create_topic,
    delete_question,
    fetch_catalog,
    fetch_question,
    fetch_questions_for_admin,
    get_active_pool,
    toggle_question,
    update_question,
)
from app.models.user import (
    delete_user,
    fetch_user_by_id,
    fetch_users,
    serialize_user,
    toggle_user_admin,
)
from app.models.room import (
    create_room,
    fetch_rooms_for_admin,
    toggle_room_active,
)
from app.parsing import parse_uploaded_file
from app.utils import admin_required


DIFFICULTIES = {"beginner", "intermediate", "advanced"}


def _redirect_with(message_type, message):
    return redirect(url_for("admin_panel", **{message_type: message}))


QUESTION_TYPES = {"mcq", "true_false", "multi_select", "fill_in_the_blank", "code_output"}


def _parse_mcq_options():
    try:
        correct_index = int(request.form.get("correct_option", "-1"))
    except ValueError as error:
        raise ValueError("Select the correct answer.") from error

    options = []
    for index in range(6):
        option_en = request.form.get(f"option_en_{index}", "").strip()
        option_ru = request.form.get(f"option_ru_{index}", "").strip()
        if not option_en and not option_ru:
            continue
        options.append({
            "text_en": option_en,
            "text_ru": option_ru,
            "is_correct": index == correct_index,
        })
    if len(options) < 2:
        raise ValueError("Provide at least two answer options.")
    if not any(option["is_correct"] for option in options):
        raise ValueError("Select the correct answer from a non-empty option.")
    return options


def _parse_multi_select_options():
    correct_indices = {
        int(value) for value in request.form.getlist("correct_options") if value.isdigit()
    }
    options = []
    for index in range(6):
        option_en = request.form.get(f"option_en_{index}", "").strip()
        option_ru = request.form.get(f"option_ru_{index}", "").strip()
        if not option_en and not option_ru:
            continue
        options.append({
            "text_en": option_en,
            "text_ru": option_ru,
            "is_correct": index in correct_indices,
        })
    if len(options) < 2:
        raise ValueError("Provide at least two answer options.")
    if not any(option["is_correct"] for option in options):
        raise ValueError("Check at least one correct option.")
    return options


def _parse_true_false_options():
    correct = request.form.get("correct_boolean", "")
    if correct not in ("true", "false"):
        raise ValueError("Select True or False as the correct answer.")
    return [
        {"text_en": "True", "text_ru": "Верно", "is_correct": correct == "true"},
        {"text_en": "False", "text_ru": "Неверно", "is_correct": correct == "false"},
    ]


def _parse_blank_options():
    answer_en = request.form.get("blank_answer_en", "").strip()
    answer_ru = request.form.get("blank_answer_ru", "").strip()
    if not answer_en and not answer_ru:
        raise ValueError("Provide the correct answer in at least one language.")
    return [{"text_en": answer_en, "text_ru": answer_ru, "is_correct": True}]


def _parse_question_form():
    topic_id = int(request.form.get("topic_id", "0"))
    text_en = request.form.get("text_en", "").strip()
    text_ru = request.form.get("text_ru", "").strip()
    if not text_en and not text_ru:
        raise ValueError("Provide the question in at least one language.")

    question_type = request.form.get("question_type", "mcq")
    if question_type not in QUESTION_TYPES:
        question_type = "mcq"

    if question_type == "multi_select":
        options = _parse_multi_select_options()
    elif question_type == "true_false":
        options = _parse_true_false_options()
    elif question_type in ("fill_in_the_blank", "code_output"):
        options = _parse_blank_options()
    else:
        options = _parse_mcq_options()

    difficulty = request.form.get("difficulty", "beginner")
    if difficulty not in DIFFICULTIES:
        difficulty = "beginner"
    pool = request.form.get("pool", "").strip() or None
    return {
        "topic_id": topic_id,
        "text_en": text_en,
        "text_ru": text_ru,
        "options": options,
        "explanation_en": request.form.get("explanation_en", "").strip(),
        "explanation_ru": request.form.get("explanation_ru", "").strip(),
        "difficulty": difficulty,
        "question_type": question_type,
        "pool": pool,
    }


def _serialize_admin_question(row):
    if row is None:
        return None
    question = dict(row)
    question["options"] = json.loads(question.pop("options_json"))
    question["is_active"] = bool(question["is_active"])
    return question


def register_admin_routes(app):
    @app.route("/admin", endpoint="admin_panel")
    @admin_required
    def admin_panel():
        user = fetch_user_by_id(session["user_id"])
        edit_question_id = request.args.get("edit_question", type=int)
        edit_question = fetch_question(edit_question_id) if edit_question_id else None
        from app.models.group import fetch_groups_for_admin
        return render_template(
            "admin.html",
            current_user=serialize_user(user),
            catalog=fetch_catalog(active_only=False),
            questions=[
                _serialize_admin_question(row) for row in fetch_questions_for_admin()
            ],
            edit_question=_serialize_admin_question(edit_question),
            users=[dict(row) for row in fetch_users()],
            rooms=[dict(row) for row in fetch_rooms_for_admin()],
            groups=[dict(row) for row in fetch_groups_for_admin()],
            active_pool=get_active_pool(),
            error=request.args.get("error"),
            success=request.args.get("success"),
        )

    @app.route("/admin/courses", methods=["POST"], endpoint="admin_create_course")
    @admin_required
    def admin_create_course():
        title_en = request.form.get("title_en", "").strip()
        title_ru = request.form.get("title_ru", "").strip()
        if not title_en or not title_ru:
            return _redirect_with("error", "Course names are required in English and Russian.")
        create_course(title_en, title_ru)
        return _redirect_with("success", "Course created.")

    @app.route("/admin/topics", methods=["POST"], endpoint="admin_create_topic")
    @admin_required
    def admin_create_topic():
        try:
            course_id = int(request.form.get("course_id", "0"))
            sort_order = int(request.form.get("sort_order", "0"))
        except ValueError:
            return _redirect_with("error", "Invalid course or sort order.")
        title_en = request.form.get("title_en", "").strip()
        title_ru = request.form.get("title_ru", "").strip()
        if not course_id or not title_en or not title_ru:
            return _redirect_with("error", "Choose a course and provide both topic names.")
        create_topic(
            course_id,
            title_en,
            title_ru,
            request.form.get("description_en", ""),
            request.form.get("description_ru", ""),
            sort_order,
        )
        return _redirect_with("success", "Topic created.")

    @app.route("/admin/questions", methods=["POST"], endpoint="admin_create_question")
    @admin_required
    def admin_create_question():
        try:
            payload = _parse_question_form()
            create_question(**payload)
        except (TypeError, ValueError) as error:
            return _redirect_with("error", str(error))
        return _redirect_with("success", "Question added to the bank.")

    @app.route(
        "/admin/questions/<int:question_id>",
        methods=["POST"],
        endpoint="admin_update_question",
    )
    @admin_required
    def admin_update_question(question_id):
        try:
            payload = _parse_question_form()
            update_question(question_id=question_id, **payload)
        except (TypeError, ValueError) as error:
            return _redirect_with("error", str(error))
        return _redirect_with("success", "Question updated.")

    @app.route(
        "/admin/questions/<int:question_id>/toggle",
        methods=["POST"],
        endpoint="admin_toggle_question",
    )
    @admin_required
    def admin_toggle_question(question_id):
        toggle_question(question_id)
        return _redirect_with("success", "Question availability updated.")

    @app.route(
        "/admin/questions/<int:question_id>/delete",
        methods=["POST"],
        endpoint="admin_delete_question",
    )
    @admin_required
    def admin_delete_question(question_id):
        delete_question(question_id)
        return _redirect_with("success", "Question deleted.")

    @app.route("/admin/import", methods=["POST"], endpoint="admin_import_questions")
    @admin_required
    def admin_import_questions():
        file = request.files.get("file")
        language = request.form.get("language", "en")
        try:
            topic_id = int(request.form.get("topic_id", "0"))
        except ValueError:
            topic_id = 0
        if not topic_id or language not in {"en", "ru"}:
            return _redirect_with("error", "Choose a topic and import language.")
        if not file or not file.filename:
            return _redirect_with("error", "Choose a PDF, DOCX, or JSON file.")
        if not file.filename.lower().endswith((".pdf", ".docx", ".json")):
            return _redirect_with("error", "Only PDF, DOCX, and JSON are supported.")
        try:
            imported = parse_uploaded_file(file.filename, file)
        except (ValueError, BadZipFile, KeyError) as error:
            return _redirect_with("error", str(error))
        except Exception:
            app.logger.exception("Question import failed")
            return _redirect_with("error", "The file could not be processed.")
        imported_count = 0
        skipped_count = 0
        for question in imported:
            options = [
                {
                    f"text_{language}": option.get("text", ""),
                    f"text_{'ru' if language == 'en' else 'en'}": "",
                    "is_correct": bool(option.get("is_correct")),
                }
                for option in question.get("options", [])
            ]
            if len(options) < 2 or not any(option["is_correct"] for option in options):
                skipped_count += 1
                continue
            create_question(
                topic_id=topic_id,
                text_en=question.get("text", "") if language == "en" else "",
                text_ru=question.get("text", "") if language == "ru" else "",
                options=options,
                explanation_en=question.get("answer_hint", "") if language == "en" else "",
                explanation_ru=question.get("answer_hint", "") if language == "ru" else "",
            )
            imported_count += 1
        if not imported_count:
            return _redirect_with(
                "error",
                "No questions with a valid answer key were found in the file.",
            )
        message = f"Imported {imported_count} questions."
        if skipped_count:
            message += f" Skipped {skipped_count} without a valid answer key."
        return _redirect_with("success", message)

    @app.route(
        "/admin/users/<int:user_id>/toggle-admin",
        methods=["POST"],
        endpoint="admin_toggle_user",
    )
    @admin_required
    def admin_toggle_user(user_id):
        if user_id == session["user_id"]:
            return _redirect_with("error", "You cannot change your own role.")
        toggle_user_admin(user_id)
        return _redirect_with("success", "User role updated.")

    @app.route(
        "/admin/users/<int:user_id>/delete",
        methods=["POST"],
        endpoint="admin_delete_user",
    )
    @admin_required
    def admin_delete_user(user_id):
        if user_id == session["user_id"]:
            return _redirect_with("error", "You cannot delete your own account.")
        delete_user(user_id)
        return _redirect_with("success", "User deleted.")

    @app.route("/admin/rooms", methods=["POST"], endpoint="admin_create_room")
    @admin_required
    def admin_create_room():
        title = request.form.get("title", "").strip()
        topic_ids = request.form.getlist("topic_ids")
        if not title or not topic_ids:
            return _redirect_with("error", "Title and at least one topic are required.")
        
        topic_ids = [int(tid) for tid in topic_ids if tid.isdigit()]
        difficulty = request.form.get("difficulty")
        if difficulty == "any":
            difficulty = None
        
        question_count = request.form.get("question_count", type=int, default=10)
        time_limit = request.form.get("time_limit", type=int)
        max_attempts = request.form.get("max_attempts", type=int)
        
        try:
            _, code = create_room(
                title=title,
                created_by=session["user_id"],
                topic_ids=topic_ids,
                difficulty=difficulty,
                question_count=question_count,
                time_limit_minutes=time_limit or None,
                max_attempts=max_attempts or None
            )
            return _redirect_with("success", f"Room created successfully! Code: {code}")
        except Exception as e:
            return _redirect_with("error", f"Failed to create room: {str(e)}")

    @app.route("/admin/rooms/<int:room_id>/toggle", methods=["POST"], endpoint="admin_toggle_room")
    @admin_required
    def admin_toggle_room(room_id):
        toggle_room_active(room_id)
        return _redirect_with("success", "Room status updated.")

    @app.route("/admin/rooms/<int:room_id>/results", endpoint="admin_room_results")
    @admin_required
    def admin_room_results(room_id):
        from app.models.room import fetch_room_by_id, fetch_room_results, analyze_room_questions
        from app.models.group import fetch_groups_for_admin
        room = fetch_room_by_id(room_id)
        if not room:
            return _redirect_with("error", "Room not found.")
            
        group_id = request.args.get("group_id", type=int)
        results = fetch_room_results(room_id, group_id=group_id)
        
        # Serialize the datetime
        serialized_results = []
        for r in results:
            d = dict(r)
            d["created_at_str"] = d["created_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(d["created_at"], "strftime") else str(d["created_at"])
            serialized_results.append(d)
            
        question_stats = analyze_room_questions(results)
        groups = fetch_groups_for_admin()
            
        return render_template(
            "room_results.html",
            current_user=serialize_user(fetch_user_by_id(session["user_id"])),
            room=dict(room),
            results=serialized_results,
            question_stats=question_stats,
            groups=[dict(g) for g in groups],
            current_group_id=group_id
        )

    @app.route("/admin/groups", methods=["POST"], endpoint="admin_create_group")
    @admin_required
    def admin_create_group():
        from app.models.group import create_group
        name = request.form.get("name", "").strip()
        if not name:
            return _redirect_with("error", "Group name is required.")
        try:
            group_id, code = create_group(name=name, created_by=session["user_id"])
            return _redirect_with("success", f"Group created successfully! Code: {code}")
        except Exception as e:
            return _redirect_with("error", f"Failed to create group: {str(e)}")


