from flask import Blueprint, request
from extensions import db
from models.notification import Notification
from utils.auth_helpers import success_response, error_response, token_required

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/<int:user_id>", methods=["GET"])
@token_required
def get_notifications(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return success_response({"notifications": [n.to_dict() for n in notifications]})

@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@token_required
def mark_read(notification_id):
    notif = Notification.query.get_or_404(notification_id)
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != notif.user_id:
        return error_response("Access forbidden", 403)
    notif.is_read = True
    db.session.commit()
    return success_response(notif.to_dict(), "Marked as read")

@notifications_bp.route("/read-all/<int:user_id>", methods=["PUT"])
@token_required
def mark_all_read(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return success_response(message="All notifications marked as read")
