import secrets

from flask import Flask, abort, jsonify, request, session
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import Config
from app.database import init_db


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    secret_key = app.config.get("SECRET_KEY")
    if not secret_key or secret_key == "change-this-secret-key":
        if not app.debug and not app.testing:
            raise RuntimeError("A strong SECRET_KEY must be set in production.")
        else:
            import logging
            logging.warning("No SECRET_KEY set. Generating an ephemeral one for development.")
            secret_key = secrets.token_hex(32)
    app.config["SECRET_KEY"] = secret_key
    app.secret_key = secret_key

    def generate_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        return session["csrf_token"]

    app.jinja_env.globals["csrf_token"] = generate_csrf_token

    @app.before_request
    def validate_csrf():
        if request.method in ("GET", "HEAD", "OPTIONS", "TRACE"):
            return
        token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
        if not token or token != session.get("csrf_token"):
            abort(403)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self';"
        if not app.debug:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
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
    from app.limiter import limiter

    limiter.init_app(app)

    register_auth_routes(app)
    register_main_routes(app)
    register_admin_routes(app)
    register_api_routes(app)

    return app
