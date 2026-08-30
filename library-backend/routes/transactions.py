from flask import Blueprint, request
from extensions import db
from models.transaction import Transaction
from models.book import Book
from models.fine import Fine
from utils.auth_helpers import success_response, error_response, token_required, role_required
from utils.fine_calculator import calculate_fine
from utils.notifications import send_notification
from config import Config
from datetime import date, timedelta

transactions_bp = Blueprint("transactions", __name__)

def _mark_overdues():
    today = date.today()
    Transaction.query.filter(
        Transaction.status == "issued",
        Transaction.due_date < today
    ).update({"status": "overdue"})
    db.session.commit()

@transactions_bp.route("/issue", methods=["POST"])
@role_required("admin", "librarian")
def issue_book():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    if not user_id or not book_id:
        return error_response("user_id and book_id are required", 400)

    book = Book.query.get_or_404(book_id)
    if book.available_copies < 1:
        return error_response("No copies available", 400)

    existing = Transaction.query.filter_by(
        user_id=user_id, book_id=book_id, status="issued"
    ).first()
    if existing:
        return error_response("User already has this book issued", 400)

    today = date.today()
    txn = Transaction(
        user_id=user_id, book_id=book_id,
        issue_date=today,
        due_date=today + timedelta(days=Config.LOAN_PERIOD_DAYS),
        status="issued",
        issued_by=request.current_user["user_id"],
    )
    book.available_copies -= 1
    db.session.add(txn)
    db.session.commit()
    send_notification(user_id, f"Book '{book.title}' issued. Due: {txn.due_date}", "general")
    return success_response(txn.to_dict(), "Book issued successfully", 201)

@transactions_bp.route("/return", methods=["POST"])
@role_required("admin", "librarian")
def return_book():
    data = request.get_json()
    transaction_id = data.get("transaction_id")
    txn = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not txn:
        return error_response("Transaction not found", 404)
    if txn.status == "returned":
        return error_response("Book already returned", 400)

    today = date.today()
    txn.return_date = today
    txn.status = "returned"

    fine_amt = calculate_fine(txn.due_date, today)
    txn.fine_amount = fine_amt

    book = Book.query.get(txn.book_id)
    book.available_copies += 1

    if fine_amt > 0:
        fine = Fine(transaction_id=txn.transaction_id, user_id=txn.user_id, amount=fine_amt)
        db.session.add(fine)
        send_notification(txn.user_id, f"Fine of ₹{fine_amt} applied for late return of '{book.title}'", "fine_alert")

    db.session.commit()
    return success_response(txn.to_dict(), "Book returned successfully")

@transactions_bp.route("", methods=["GET"])
@role_required("admin", "librarian")
def get_all_transactions():
    _mark_overdues()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    status = request.args.get("status")
    query = Transaction.query
    if status:
        query = query.filter_by(status=status)
    paginated = query.order_by(Transaction.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return success_response({
        "transactions": [t.to_dict() for t in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
    })

@transactions_bp.route("/user/<int:user_id>", methods=["GET"])
@token_required
def user_transactions(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    _mark_overdues()
    txns = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    return success_response({"transactions": [t.to_dict() for t in txns]})

@transactions_bp.route("/overdue", methods=["GET"])
@role_required("admin", "librarian")
def overdue_transactions():
    _mark_overdues()
    txns = Transaction.query.filter_by(status="overdue").all()
    return success_response({"transactions": [t.to_dict() for t in txns], "count": len(txns)})

@transactions_bp.route("/<int:transaction_id>/status", methods=["PUT"])
@role_required("admin", "librarian")
def update_status(transaction_id):
    txn = Transaction.query.get_or_404(transaction_id)
    data = request.get_json()
    if data.get("status") in ("issued", "returned", "overdue"):
        txn.status = data["status"]
        db.session.commit()
    return success_response(txn.to_dict(), "Status updated")
