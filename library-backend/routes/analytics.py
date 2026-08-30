from flask import Blueprint
from extensions import db
from models.book import Book
from models.transaction import Transaction
from models.user import User
from models.fine import Fine
from utils.auth_helpers import success_response, role_required
from sqlalchemy import func, extract
from datetime import date, timedelta

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/dashboard", methods=["GET"])
@role_required("admin", "librarian")
def dashboard():
    total_books = Book.query.count()
    total_members = User.query.filter_by(role="student", is_active=True).count()
    books_issued = Transaction.query.filter(Transaction.status.in_(["issued", "overdue"])).count()
    overdue_count = Transaction.query.filter_by(status="overdue").count()
    fines_pending = db.session.query(func.sum(Fine.amount)).filter_by(paid=False).scalar() or 0
    fines_collected = db.session.query(func.sum(Fine.amount)).filter_by(paid=True).scalar() or 0
    return success_response({
        "total_books": total_books,
        "total_members": total_members,
        "books_issued": books_issued,
        "overdue_count": overdue_count,
        "fines_pending": float(fines_pending),
        "fines_collected": float(fines_collected),
    })

@analytics_bp.route("/monthly-issues", methods=["GET"])
@role_required("admin", "librarian")
def monthly_issues():
    results = (
        db.session.query(
            extract("year", Transaction.issue_date).label("year"),
            extract("month", Transaction.issue_date).label("month"),
            func.count(Transaction.transaction_id).label("count"),
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .limit(12)
        .all()
    )
    data = [{"year": int(r.year), "month": int(r.month), "count": r.count} for r in results]
    return success_response({"monthly_issues": data})

@analytics_bp.route("/genre-distribution", methods=["GET"])
@role_required("admin", "librarian")
def genre_distribution():
    results = (
        db.session.query(Book.genre, func.count(Book.book_id).label("count"))
        .filter(Book.genre.isnot(None))
        .group_by(Book.genre)
        .all()
    )
    data = [{"genre": r.genre, "count": r.count} for r in results]
    return success_response({"genre_distribution": data})

@analytics_bp.route("/top-books", methods=["GET"])
@role_required("admin", "librarian")
def top_books():
    results = (
        db.session.query(Book, func.count(Transaction.transaction_id).label("borrow_count"))
        .join(Transaction, Transaction.book_id == Book.book_id)
        .group_by(Book.book_id)
        .order_by(func.count(Transaction.transaction_id).desc())
        .limit(10)
        .all()
    )
    data = [{**b.to_dict(), "borrow_count": count} for b, count in results]
    return success_response({"top_books": data})

@analytics_bp.route("/overdue-trends", methods=["GET"])
@role_required("admin", "librarian")
def overdue_trends():
    results = (
        db.session.query(
            extract("year", Transaction.due_date).label("year"),
            extract("month", Transaction.due_date).label("month"),
            func.count(Transaction.transaction_id).label("count"),
        )
        .filter(Transaction.status == "overdue")
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    data = [{"year": int(r.year), "month": int(r.month), "count": r.count} for r in results]
    return success_response({"overdue_trends": data})
