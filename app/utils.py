import secrets
from functools import wraps

from flask import abort, redirect, request, session, url_for


UI_STRINGS = {
    "en": {
        "start": "Start",
        "username": "Username",
        "password": "Password",
        "login": "Log in",
        "register": "Register",
        "logout": "Log out",
        "profile": "Profile",
        "your_profile": "YOUR PROFILE",
        "teacher_panel": "Teacher panel",
        "save": "Save",
        "cancel": "Cancel",
    },
    "ru": {
        "start": "Начать",
        "username": "Имя пользователя",
        "password": "Пароль",
        "login": "Войти",
        "register": "Регистрация",
        "logout": "Выйти",
        "profile": "Профиль",
        "your_profile": "ВАШ ПРОФИЛЬ",
        "teacher_panel": "Панель преподавателя",
        "save": "Сохранить",
        "cancel": "Отмена",
    }
}



def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf():
    if request.method in ("GET", "HEAD", "OPTIONS", "TRACE"):
        return
    token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
    if not token or token != session.get("csrf_token"):
        if request.path.startswith("/api/"):
            from flask import jsonify
            return jsonify({"error": "csrf_failed"}), 403
        abort(403)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                from flask import jsonify
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app.models.user import fetch_user_by_id
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                from flask import jsonify
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("login"))
        user = fetch_user_by_id(session["user_id"])
        if not user or not user["is_admin"]:
            if request.path.startswith("/api/"):
                from flask import jsonify
                return jsonify({"error": "Forbidden"}), 403
            abort(403)
        return f(*args, **kwargs)
    return decorated
