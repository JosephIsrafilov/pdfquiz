from flask import redirect, render_template, session, url_for

from app.models.knowledge import fetch_catalog
from app.models.result import build_attempt_review, fetch_result_for_user, fetch_results_for_user, serialize_result
from app.models.user import fetch_user_by_id, serialize_user
from app.utils import login_required


def register_main_routes(app):
    @app.route("/", endpoint="index")
    def index():
        user = None
        if "user_id" in session:
            user = fetch_user_by_id(session["user_id"])
        return render_template(
            "index.html",
            current_user=serialize_user(user) if user else None,
            catalog=fetch_catalog(),
        )

    @app.route("/profile", endpoint="profile")
    @login_required
    def profile():
        user = fetch_user_by_id(session["user_id"])
        results = fetch_results_for_user(user["id"])
        return render_template(
            "profile.html",
            current_user=serialize_user(user),
            results=[serialize_result(r) for r in results],
        )

    @app.route("/profile/results/<int:result_id>", endpoint="profile_result_detail")
    @login_required
    def profile_result_detail(result_id):
        user = fetch_user_by_id(session["user_id"])
        result = fetch_result_for_user(result_id, user["id"])
        if result is None:
            from flask import abort
            abort(404)
        return render_template(
            "result_detail.html",
            current_user=serialize_user(user),
            result=serialize_result(result),
            review=build_attempt_review(result),
        )
