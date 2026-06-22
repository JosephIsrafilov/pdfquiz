from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.models.user import create_user, fetch_user_by_username, serialize_user
from app.utils import login_required


def register_auth_routes(app):
    @app.route("/login", methods=["GET", "POST"], endpoint="login")
    def login():
        if request.method == "GET":
            return render_template("login.html")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = fetch_user_by_username(username)
        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Неверный логин или пароль")
        session["user_id"] = user["id"]
        return redirect(url_for("index"))

    @app.route("/register", methods=["GET", "POST"], endpoint="register")
    def register():
        if request.method == "GET":
            return render_template("register.html")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return render_template("register.html", error="Заполните все поля")
        if fetch_user_by_username(username):
            return render_template("register.html", error="Имя уже занято")
        try:
            user = create_user(username, password)
        except Exception:
            return render_template("register.html", error="Ошибка при создании аккаунта")
        session["user_id"] = user["id"]
        return redirect(url_for("index"))

    @app.route("/logout", methods=["POST"], endpoint="logout")
    @login_required
    def logout():
        session.clear()
        return redirect(url_for("login"))
