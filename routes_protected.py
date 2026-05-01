from flask import Blueprint, jsonify
from auth import require_auth, require_role

protected_bp = Blueprint("protected", __name__)


@protected_bp.route("/me", methods=["GET"])
@require_auth
def me():
    return jsonify({
        "user_id": request.user["sub"],
        "roles": request.user["roles"]
    })


@protected_bp.route("/admin/dashboard", methods=["GET"])
@require_auth
@require_role("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome, Admin"})
