from flask import Blueprint, redirect

bp = Blueprint("view", __name__)


@bp.route("/")
def index():
    """Redirect root to the API docs or SPA."""
    return redirect("/api/jobs")
