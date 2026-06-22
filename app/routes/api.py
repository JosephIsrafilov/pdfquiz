import json
from zipfile import BadZipFile

from flask import jsonify, request, session

from app.models.document import fetch_document
from app.models.result import fetch_results_for_user, save_result, serialize_result
from app.models.user import fetch_user_by_id
from app.utils import login_required
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

    @app.route("/api/parse", methods=["POST"], endpoint="parse_document")
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
            questions = json.loads(document["questions_json"])
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

    @app.route("/api/results", methods=["POST"], endpoint="save_quiz_result")
    @login_required
    def save_quiz_result():
        payload = request.get_json(silent=True) or {}
        required_keys = {
            "source_label", "total_questions", "quiz_size", "graded", "correct",
            "unanswered", "missing_answer_key", "mistake_numbers", "attempt",
        }
        if not required_keys.issubset(payload.keys()):
            return jsonify({"error": "Недостаточно данных для сохранения результата."}), 400
        user = fetch_user_by_id(session["user_id"])
        save_result(
            user_id=user["id"],
            document_id=payload.get("document_id"),
            source_label=str(payload["source_label"]),
            total_questions=int(payload["total_questions"]),
            quiz_size=int(payload["quiz_size"]),
            graded=int(payload["graded"]),
            correct=int(payload["correct"]),
            unanswered=int(payload["unanswered"]),
            missing_answer_key=int(payload["missing_answer_key"]),
            mistake_numbers=[int(v) for v in payload.get("mistake_numbers", [])],
            attempt_payload=payload.get("attempt"),
        )
        latest = fetch_results_for_user(user["id"], limit=1)
        return jsonify({"ok": True, "result": serialize_result(latest[0]) if latest else None})
