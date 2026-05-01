from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import User
from auth import create_access_token, create_refresh_token, decode_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    roles = [role.name for role in user.roles]

    access = create_access_token(user.id, roles)
    refresh = create_refresh_token(user.id)

    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "roles": roles
    })


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.json
    token = data.get("refresh_token")

    decoded = decode_token(token)
    if not decoded or decoded.get("type") != "refresh":
        return jsonify({"error": "Invalid refresh token"}), 401

    user_id = decoded["sub"]

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    roles = [role.name for role in user.roles]

    new_access = create_access_token(user.id, roles)

    return jsonify({"access_token": new_access})
