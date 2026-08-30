from flask import Blueprint, request
from extensions import db
from models.reservation import Reservation
from models.book import Book
from utils.auth_helpers import success_response, error_response, token_required
from utils.notifications import send_notification
from datetime import datetime, timedelta

reservations_bp = Blueprint("reservations", __name__)

def _expire_old():
    now = datetime.utcnow()
    Reservation.query.filter(
        Reservation.status == "pending",
        Reservation.expires_at < now
    ).update({"status": "cancelled"})
    db.session.commit()

@reservations_bp.route("", methods=["POST"])
@token_required
def reserve_book():
    _expire_old()
    data = request.get_json()
    user_id = data.get("user_id") or request.current_user["user_id"]
    book_id = data.get("book_id")
    if not book_id:
        return error_response("book_id is required", 400)

    book = Book.query.get_or_404(book_id)
    existing = Reservation.query.filter_by(user_id=user_id, book_id=book_id, status="pending").first()
    if existing:
        return error_response("Already reserved", 400)

    now = datetime.utcnow()
    reservation = Reservation(
        user_id=user_id, book_id=book_id,
        reserved_at=now,
        expires_at=now + timedelta(days=3),
        status="pending",
    )
    db.session.add(reservation)
    db.session.commit()
    send_notification(user_id, f"Reservation placed for '{book.title}'. Expires in 3 days.", "reservation")
    return success_response(reservation.to_dict(), "Book reserved", 201)

@reservations_bp.route("/user/<int:user_id>", methods=["GET"])
@token_required
def user_reservations(user_id):
    _expire_old()
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.reserved_at.desc()).all()
    return success_response({"reservations": [r.to_dict() for r in reservations]})

@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"])
@token_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != reservation.user_id:
        return error_response("Access forbidden", 403)
    reservation.status = "cancelled"
    db.session.commit()
    return success_response(message="Reservation cancelled")
