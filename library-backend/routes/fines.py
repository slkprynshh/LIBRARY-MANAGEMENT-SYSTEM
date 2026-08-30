from flask import Blueprint, request
from extensions import db
from models.fine import Fine
from utils.auth_helpers import success_response, error_response, token_required, role_required
from datetime import datetime
from sqlalchemy import func

fines_bp = Blueprint("fines", __name__)

@fines_bp.route("", methods=["GET"])
@role_required("admin", "librarian")
def get_all_fines():
    fines = Fine.query.order_by(Fine.created_at.desc()).all()
    return success_response({"fines": [f.to_dict() for f in fines]})

@fines_bp.route("/user/<int:user_id>", methods=["GET"])
@token_required
def user_fines(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    fines = Fine.query.filter_by(user_id=user_id).all()
    return success_response({"fines": [f.to_dict() for f in fines]})

@fines_bp.route("/pay/<int:fine_id>", methods=["POST"])
@role_required("admin", "librarian")
def pay_fine(fine_id):
    fine = Fine.query.get_or_404(fine_id)
    if fine.paid:
        return error_response("Fine already paid", 400)
    fine.paid = True
    fine.paid_at = datetime.utcnow()
    db.session.commit()
    return success_response(fine.to_dict(), "Fine marked as paid")

@fines_bp.route("/summary", methods=["GET"])
@role_required("admin", "librarian")
def fine_summary():
    total = db.session.query(func.sum(Fine.amount)).scalar() or 0
    collected = db.session.query(func.sum(Fine.amount)).filter_by(paid=True).scalar() or 0
    pending = db.session.query(func.sum(Fine.amount)).filter_by(paid=False).scalar() or 0
    return success_response({
        "total_fines": float(total),
        "collected": float(collected),
        "pending": float(pending),
        "total_count": Fine.query.count(),
        "paid_count": Fine.query.filter_by(paid=True).count(),
        "unpaid_count": Fine.query.filter_by(paid=False).count(),
    })
