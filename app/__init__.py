import secrets

from flask import Flask, abort, jsonify, request, session
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import Config
from app.database import init_db


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    def generate_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        return session["csrf_token"]

    app.jinja_env.globals["csrf_token"] = generate_csrf_token

    @app.before_request
    def validate_csrf():
        if request.method in ("GET", "HEAD", "OPTIONS", "TRACE"):
            return
        if request.path.startswith("/api/"):
            return
        content_type = request.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return
        token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
        if not token or token != session.get("csrf_token"):
            abort(403)

    @app.after_request
    def add_ngrok_skip_header(response):
        response.headers["ngrok-skip-browser-warning"] = "true"
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(_error):
        return jsonify({"error": "Файл слишком большой. Максимум 25 МБ."}), 413

    init_db()
    from app.models.knowledge import synchronize_python_curriculum
    synchronize_python_curriculum()

    from app.routes.auth import register_auth_routes
    from app.routes.main import register_main_routes
    from app.routes.admin import register_admin_routes
    from app.routes.api import register_api_routes

    register_auth_routes(app)
    register_main_routes(app)
    register_admin_routes(app)
    register_api_routes(app)

    return app
