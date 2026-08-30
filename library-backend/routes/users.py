from flask import Blueprint, request
from extensions import db
from models.user import User
from utils.auth_helpers import success_response, error_response, token_required, role_required
import bcrypt

users_bp = Blueprint("users", __name__)

@users_bp.route("", methods=["GET"])
@role_required("admin")
def get_all_users():
    role = request.args.get("role")
    query = User.query
    if role:
        query = query.filter_by(role=role)
    users = query.order_by(User.created_at.desc()).all()
    return success_response({"users": [u.to_dict() for u in users]})

@users_bp.route("/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    user = User.query.get_or_404(user_id)
    return success_response(user.to_dict())

@users_bp.route("", methods=["POST"])
@role_required("admin")
def create_user():
    data = request.get_json()
    if User.query.filter_by(email=data.get("email")).first():
        return error_response("Email already exists", 409)
    user = User(
        name=data["name"], email=data["email"],
        password_hash=bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode(),
        role=data.get("role", "student"),
        department=data.get("department"),
        phone=data.get("phone"),
    )
    db.session.add(user)
    db.session.commit()
    return success_response(user.to_dict(), "User created", 201)

@users_bp.route("/<int:user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    for field in ["name", "department", "phone", "profile_pic"]:
        if field in data:
            setattr(user, field, data[field])
    if current["role"] == "admin" and "role" in data:
        user.role = data["role"]
    db.session.commit()
    return success_response(user.to_dict(), "User updated")

@users_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required("admin")
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return success_response(message="User deactivated")
