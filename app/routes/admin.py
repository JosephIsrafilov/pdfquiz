import json
from zipfile import BadZipFile

from flask import jsonify, redirect, render_template, request, session, url_for

from app.models.document import (
    delete_document,
    fetch_document,
    fetch_documents,
    save_document,
    serialize_document,
)
from app.models.user import delete_user, fetch_user_by_id, fetch_users, serialize_user, toggle_user_admin
from app.utils import admin_required
from app.parsing import parse_uploaded_file


def register_admin_routes(app):
    @app.route("/admin", endpoint="admin_panel")
    @admin_required
    def admin_panel():
        user = fetch_user_by_id(session["user_id"])
        documents = fetch_documents()
        users = fetch_users()
        return render_template(
            "admin.html",
            current_user=serialize_user(user),
            documents=[serialize_document(d) for d in documents],
            users=[dict(u) for u in users],
            error=request.args.get("error"),
            success=request.args.get("success"),
        )

    @app.route("/admin/documents", methods=["POST"], endpoint="admin_upload_document")
    @admin_required
    def admin_upload_document():
        title = request.form.get("title", "").strip()
        file = request.files.get("file")
        if not file or not file.filename:
            return redirect(url_for("admin_panel", error="Файл не выбран"))
        filename = file.filename.lower()
        if not filename.endswith((".pdf", ".docx", ".json")):
            return redirect(url_for("admin_panel", error="Поддерживаются только PDF, DOCX и JSON"))
        try:
            questions = parse_uploaded_file(filename, file)
        except ValueError as e:
            return redirect(url_for("admin_panel", error=str(e)))
        except BadZipFile:
            return redirect(url_for("admin_panel", error="DOCX файл поврежден или имеет неверный формат"))
        except KeyError:
            return redirect(url_for("admin_panel", error="Не удалось прочитать структуру DOCX"))
        except Exception:
            return redirect(url_for("admin_panel", error="Не удалось прочитать файл"))
        if not questions:
            return redirect(url_for("admin_panel", error="Не удалось распознать вопросы"))
        doc_title = title or file.filename
        save_document(doc_title, json.dumps(questions), session["user_id"])
        return redirect(url_for("admin_panel", success=f"Загружено: {doc_title}"))

    @app.route("/admin/documents/<int:document_id>/delete", methods=["POST"], endpoint="admin_delete_document")
    @admin_required
    def admin_delete_document(document_id):
        delete_document(document_id)
        return redirect(url_for("admin_panel", success="Документ удалён"))

    @app.route("/admin/users/<int:user_id>/toggle-admin", methods=["POST"], endpoint="admin_toggle_user")
    @admin_required
    def admin_toggle_user(user_id):
        toggle_user_admin(user_id)
        return redirect(url_for("admin_panel"))

    @app.route("/admin/users/<int:user_id>/delete", methods=["POST"], endpoint="admin_delete_user")
    @admin_required
    def admin_delete_user(user_id):
        if user_id == session["user_id"]:
            return redirect(url_for("admin_panel", error="Нельзя удалить свой аккаунт"))
        delete_user(user_id)
        return redirect(url_for("admin_panel", success="Пользователь удалён"))
