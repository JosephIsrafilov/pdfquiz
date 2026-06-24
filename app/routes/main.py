from datetime import datetime

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
        serialized = [serialize_result(r) for r in results]

        from app.models.group import fetch_user_groups
        raw_user_groups = fetch_user_groups(user["id"])
        user_groups = []
        for group in raw_user_groups:
            serialized_group = dict(group)
            joined_at = serialized_group.get("joined_at")
            if isinstance(joined_at, datetime):
                serialized_group["joined_at"] = joined_at.strftime("%Y-%m-%d %H:%M:%S")
            elif joined_at is not None:
                serialized_group["joined_at"] = str(joined_at)
            user_groups.append(serialized_group)

        total_tests = len(serialized)
        total_questions = sum(r["graded"] for r in serialized)
        total_correct = sum(r["correct"] for r in serialized)
        average_score = round((total_correct / total_questions) * 100) if total_questions > 0 else 0

        import json

        from flask import request
        return render_template(
            "profile.html",
            current_user=serialize_user(user),
            results=serialized,
            user_groups=user_groups,
            stats={
                "total_tests": total_tests,
                "total_questions": total_questions,
                "average_score": average_score
            },
            results_json=json.dumps(serialized),
            error=request.args.get("error"),
            success=request.args.get("success")
        )

    @app.route("/profile/join-group", methods=["POST"], endpoint="profile_join_group")
    @login_required
    def profile_join_group():
        from flask import request
        from app.models.group import join_group
        code = request.form.get("code", "").strip().upper()
        if not code:
            return redirect(url_for("profile", error="Please enter a group code."))
        
        success, message = join_group(code, session["user_id"])
        if success:
            return redirect(url_for("profile", success=message))
        else:
            return redirect(url_for("profile", error=message))

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
