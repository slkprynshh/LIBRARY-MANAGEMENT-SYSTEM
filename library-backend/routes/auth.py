from flask import Blueprint, request
from extensions import db
from models.user import User
from utils.auth_helpers import success_response, error_response, decode_token, token_required
from config import Config
from datetime import datetime, timedelta
import bcrypt, jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return error_response("Email and password required", 400)
    user = User.query.filter_by(email=data["email"], is_active=True).first()
    if not user or not bcrypt.checkpw(data["password"].encode(), user.password_hash.encode()):
        return error_response("Invalid credentials", 401)
    payload = {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS),
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return success_response({"token": token, "user": user.to_dict()}, "Login successful")

@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    return success_response(message="Logged out successfully")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required = ["name", "email", "password"]
    if not all(data.get(f) for f in required):
        return error_response("name, email, and password are required", 400)
    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already registered", 409)
    user = User(
        name=data["name"], email=data["email"],
        password_hash=bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode(),
        role="student",
        department=data.get("department"),
        phone=data.get("phone"),
    )
    db.session.add(user)
    db.session.commit()
    return success_response(user.to_dict(), "Registration successful", 201)

@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    user = User.query.get(request.current_user["user_id"])
    if not user:
        return error_response("User not found", 404)
    return success_response(user.to_dict())

@auth_bp.route("/change-password", methods=["PUT"])
@token_required
def change_password():
    data = request.get_json()
    user = User.query.get(request.current_user["user_id"])
    if not bcrypt.checkpw(data.get("old_password", "").encode(), user.password_hash.encode()):
        return error_response("Current password is incorrect", 400)
    user.password_hash = bcrypt.hashpw(data["new_password"].encode(), bcrypt.gensalt()).decode()
    db.session.commit()
    return success_response(message="Password changed successfully")
