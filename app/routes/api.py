import json
from zipfile import BadZipFile

from flask import jsonify, request, session

from app.models.document import fetch_document
from app.models.quiz import check_quiz_question, create_quiz, submit_quiz
from app.models.result import (
    fetch_result_for_user,
    fetch_results_for_user,
    save_result,
    serialize_result,
)
from app.models.user import fetch_user_by_id
from app.utils import login_required
from app.limiter import limiter
from app.parsing import parse_uploaded_file


def register_api_routes(app):
    @app.route("/health", methods=["GET"], endpoint="health")
    def health():
        from app.database import get_db_connection
        try:
            with get_db_connection() as conn:
                conn.execute("SELECT 1")
            db_status = "connected"
        except Exception as exc:
            db_status = f"error: {exc}"
        return jsonify({"status": "ok", "db": db_status})

    @app.route("/api/quizzes", methods=["POST"], endpoint="create_topic_quiz")
    def create_topic_quiz():
        payload = request.get_json(silent=True) or {}
        topic_ids = payload.get("topic_ids")
        if not isinstance(topic_ids, list) or not topic_ids:
            return jsonify({"error": "Select at least one topic."}), 400
        try:
            quiz = create_quiz(
                topic_ids=topic_ids,
                count=int(payload.get("count", 10)),
                language=str(payload.get("language", "en")),
                difficulty=str(payload.get("difficulty", "all")),
                user_id=session.get("user_id"),
            )
        except (TypeError, ValueError) as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(quiz), 201

    @app.route("/api/quizzes/room", methods=["POST"], endpoint="create_room_quiz")
    def create_room_quiz():
        payload = request.get_json(silent=True) or {}
        code = payload.get("code")
        if not code:
            return jsonify({"error": "Room code is required."}), 400
        try:
            from app.models.quiz import create_quiz_from_room
            quiz = create_quiz_from_room(
                code=code,
                language=str(payload.get("language", "en")),
                user_id=session.get("user_id"),
            )
        except (TypeError, ValueError) as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(quiz), 201

    @app.route(
        "/api/quizzes/<token>/check",
        methods=["POST"],
        endpoint="check_topic_quiz_question",
    )
    def check_topic_quiz_question(token):
        payload = request.get_json(silent=True) or {}
        try:
            result = check_quiz_question(
                token=token,
                question_id=int(payload.get("question_id")),
                selected=payload.get("selected"),
                user_id=session.get("user_id"),
            )
        except PermissionError as error:
            return jsonify({"error": str(error)}), 403
        except (TypeError, ValueError) as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(result)

    @app.route(
        "/api/quizzes/<token>/submit",
        methods=["POST"],
        endpoint="submit_topic_quiz",
    )
    def submit_topic_quiz(token):
        payload = request.get_json(silent=True) or {}
        answers = payload.get("answers", {})
        if not isinstance(answers, dict):
            return jsonify({"error": "Answers must be an object."}), 400
        try:
            result = submit_quiz(token, answers, session.get("user_id"))
        except PermissionError as error:
            return jsonify({"error": str(error)}), 403
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        saved_result = None
        if session.get("user_id"):
            mistake_numbers = [
                index
                for index, item in enumerate(result["review"], start=1)
                if not item["is_correct"]
            ]
            result_id = save_result(
                user_id=session["user_id"],
                document_id=None,
                source_label=result["source_label"],
                total_questions=result["total"],
                quiz_size=result["total"],
                graded=result["total"],
                correct=result["correct"],
                unanswered=result["unanswered"],
                missing_answer_key=0,
                mistake_numbers=mistake_numbers,
                attempt_payload=result["review"],
                room_id=result.get("room_id"),
            )
            latest = fetch_result_for_user(result_id, session["user_id"]) if result_id else None
            saved_result = serialize_result(latest) if latest else None
        return jsonify({"result": result, "saved_result": saved_result})

    @app.route("/api/parse", methods=["POST"], endpoint="parse_document")
    @limiter.limit(lambda: app.config["PARSE_RATE_LIMIT"])
    @login_required
    def parse_document():
        document_id_raw = request.form.get("document_id", "").strip()
        source_label = "Загруженный файл"
        document_id = None
        if document_id_raw:
            try:
                document_id = int(document_id_raw)
            except ValueError:
                return jsonify({"error": "Некорректный документ"}), 400
            document = fetch_document(document_id)
            if document is None:
                return jsonify({"error": "Документ не найден"}), 404
                
            user = fetch_user_by_id(session["user_id"])
            if not user["is_admin"] and document["uploaded_by"] != user["id"]:
                return jsonify({"error": "Forbidden"}), 403
                
            try:
                questions = json.loads(document["questions_json"])
            except json.JSONDecodeError:
                return jsonify({"error": "Некорректный JSON"}), 400
                
            source_label = document["title"]
        else:
            if "file" not in request.files:
                return jsonify({"error": "Файл не найден"}), 400
            file = request.files["file"]
            if not file or not file.filename:
                return jsonify({"error": "Файл не выбран"}), 400
            filename = file.filename.lower()
            if not filename.endswith((".pdf", ".docx", ".json")):
                return jsonify({"error": "Поддерживаются только PDF, DOCX и JSON"}), 400
            try:
                questions = parse_uploaded_file(filename, file)
                source_label = file.filename
            except ValueError as error:
                return jsonify({"error": str(error)}), 400
            except BadZipFile:
                return jsonify({"error": "DOCX файл поврежден или имеет неверный формат"}), 400
            except KeyError:
                return jsonify({"error": "Не удалось прочитать структуру DOCX"}), 400
            except Exception:
                return jsonify({"error": "Не удалось прочитать файл"}), 500
        if not questions:
            return jsonify({"error": "Не удалось распознать вопросы"}), 400
        return jsonify({
            "count": len(questions),
            "questions": questions,
            "document_id": document_id,
            "source_label": source_label,
        })

