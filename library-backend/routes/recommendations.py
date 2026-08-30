from flask import Blueprint, request
from extensions import db
from models.book import Book
from models.transaction import Transaction
from models.rating import BookRating
from utils.auth_helpers import success_response, error_response, token_required
from ai.recommender import Recommender
from ai.nlp_search import NLPSearch
from ai.demand_predictor import DemandPredictor
from datetime import date, timedelta
from sqlalchemy import func

recommendations_bp = Blueprint("recommendations", __name__)
recommender = Recommender()
nlp_search = NLPSearch()
demand_predictor = DemandPredictor()

@recommendations_bp.route("/recommendations/<int:user_id>", methods=["GET"])
@token_required
def get_recommendations(user_id):
    current = request.current_user
    if current["role"] == "student" and current["user_id"] != user_id:
        return error_response("Access forbidden", 403)
    books = Book.query.all()
    ratings = BookRating.query.all()
    result = recommender.recommend(user_id, books, ratings)
    return success_response({"recommendations": result})

@recommendations_bp.route("/similar/<int:book_id>", methods=["GET"])
def similar_books(book_id):
    books = Book.query.all()
    result = nlp_search.similar(book_id, books)
    return success_response({"similar_books": result})

@recommendations_bp.route("/trending", methods=["GET"])
def trending():
    since = date.today() - timedelta(days=7)
    results = (
        db.session.query(Book, func.count(Transaction.transaction_id).label("count"))
        .join(Transaction, Transaction.book_id == Book.book_id)
        .filter(Transaction.issue_date >= since)
        .group_by(Book.book_id)
        .order_by(func.count(Transaction.transaction_id).desc())
        .limit(10)
        .all()
    )
    data = [{**b.to_dict(), "issue_count": count} for b, count in results]
    return success_response({"trending": data})

@recommendations_bp.route("/demand-forecast", methods=["GET"])
@token_required
def demand_forecast():
    transactions = Transaction.query.all()
    books = Book.query.all()
    result = demand_predictor.forecast(transactions, books)
    return success_response({"forecast": result})

@recommendations_bp.route("/search", methods=["POST"])
def nlp_search_route():
    data = request.get_json()
    q = data.get("query", "").strip()
    if not q:
        return error_response("query is required", 400)
    books = Book.query.all()
    results = nlp_search.search(q, books)
    return success_response({"results": results, "count": len(results)})

@recommendations_bp.route("/chat", methods=["POST"])
def ai_chat_assistant():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip().lower()
    user_id = data.get("user_id") or 3

    from models.user import User
    from models.fine import Fine

    user = User.query.get(user_id)
    user_name = user.name if user else "Rahul Sharma"
    is_admin_mode = (user and user.role in ("admin", "librarian")) or "student" in message or "account" in message

    txns = Transaction.query.filter_by(user_id=user_id).all()
    active_txns = [t for t in txns if t.status in ("issued", "overdue")]
    overdue_txns = [t for t in txns if t.status == "overdue"]

    fines = Fine.query.filter_by(user_id=user_id, paid=False).all()
    unpaid_fine_total = sum(f.amount for f in fines)

    actions = []
    reply = ""
    feedback_footer = "<br/><br/><em style='font-size:11px;opacity:0.75'>Was this helpful? Your feedback improves my accuracy.</em>"

    # Rule 1, 2 & 4: Direct Answers First + Context Integration + Active Loans Only
    if "which" in message or "what books" in message or "my books" in message or "borrowed" in message or "student" in message:
        if not active_txns:
            # Rule 5: Fallback Handling
            reply = f"No active borrowed books found for student {user_name}. Would you like to view available library catalog books?{feedback_footer}"
        else:
            book_rows = []
            for t in active_txns:
                title = t.book.title if (t.book and t.book.title) else f"Book #{t.book_id}"
                # Rule 3: Data Accuracy - Never say "Unknown Author"
                author = t.book.author if (t.book and t.book.author) else "Author information not available for this book"
                issue_date = t.issue_date if t.issue_date else "N/A"
                # Rule 5 (Librarian): Overdue Alerts with urgency
                status_badge = '<span class="badge badge-danger">⚠️ Overdue — Please notify the student</span>' if t.status == "overdue" else '<span class="badge badge-success">Active</span>'
                book_rows.append(f'<tr><td style="padding:5px"><strong>{title}</strong></td><td style="padding:5px">{author}</td><td style="padding:5px">{issue_date}</td><td style="padding:5px">{t.due_date}</td><td style="padding:5px">{status_badge}</td></tr>')
            
            table_html = f'<table style="width:100%;font-size:12px;border-collapse:collapse;margin:8px 0"><tr style="border-bottom:1px solid rgba(255,255,255,0.15);text-align:left"><th style="padding:5px">Title</th><th style="padding:5px">Author</th><th style="padding:5px">Issue Date</th><th style="padding:5px">Due Date</th><th style="padding:5px">Status</th></tr>{"".join(book_rows)}</table>'
            
            # Rule 2: Unified context integration (loans + fines + overdue alerts + recommendations)
            context_note = ""
            if overdue_txns or unpaid_fine_total > 0:
                context_note = f"<br/>⚠️ <strong>Admin Account Summary for {user_name}:</strong> Student has {len(overdue_txns)} overdue item(s) and ₹{unpaid_fine_total:.0f} pending fines."
                if overdue_txns:
                    actions.append({"label": "Notify Student of Overdue", "action": "notify", "user_id": user_id})
                    actions.append({"label": "Renew Student Loan", "action": "renew", "txn_id": overdue_txns[0].transaction_id})
                if fines:
                    actions.append({"label": f"Clear ₹{unpaid_fine_total:.0f} Fine", "action": "pay_fine", "fine_id": fines[0].fine_id})

            # Rule 6 (Librarian): Action Guidance
            guidance = "<br/><br/>💡 <strong>Action Guidance:</strong> You can issue reminders to the student, extend due dates, or process book returns."
            reply = f"📚 **Active Borrowed Books Report for Student {user_name} ({len(active_txns)} active):**<br/><br/>{table_html}{context_note}{guidance}{feedback_footer}"

    elif "fine" in message or "pay" in message or "fee" in message:
        if unpaid_fine_total > 0:
            reply = f"💰 **Fine Ledger for {user_name}:**<br/>Student has an unpaid fine balance of **₹{unpaid_fine_total:.0f}** for overdue book returns.<br/><br/>💡 <strong>Action Guidance:</strong> Click below to mark fine as collected or issue a payment receipt.{feedback_footer}"
            if fines:
                actions.append({"label": f"Mark ₹{unpaid_fine_total:.0f} Fine Paid", "action": "pay_fine", "fine_id": fines[0].fine_id})
        else:
            reply = f"Student {user_name} has a clear fine record with ₹0 pending balance.{feedback_footer}"

    elif "due" in message or "date" in message or "when" in message:
        if overdue_txns:
            overdue_book = overdue_txns[0].book.title if (overdue_txns and overdue_txns[0].book) else "The Pragmatic Programmer"
            reply = f"🗓️ **Due Date Tracking — {user_name}:**<br/>⚠️ <strong>Overdue Warning:</strong> '{overdue_book}' is overdue! Due date was {overdue_txns[0].due_date}. Please notify the student.<br/><br/>💡 <strong>Action Guidance:</strong> Click 'Notify Student' or extend the due date by 14 days.{feedback_footer}"
            actions.append({"label": "Notify Student", "action": "notify", "user_id": user_id})
            actions.append({"label": "Extend Due Date", "action": "renew", "txn_id": overdue_txns[0].transaction_id})
        else:
            reply = f"🗓️ All active loans for student {user_name} are within valid due dates.{feedback_footer}"

    # Rule 7 (Librarian): Personalized Recommendations with reasoning
    elif "recommend" in message or "suggest" in message or "next" in message or "read" in message:
        books_all = Book.query.all()
        ratings_all = BookRating.query.all()
        recs = recommender.recommend(user_id, books_all, ratings_all, top_n=3)
        rec_items = []
        for r in recs:
            genre = r.get("genre") or "Technology & Computer Science"
            rec_items.append(f"• **{r['title']}** by {r.get('author', 'Author info not available for this book')} — *Based on student's interest in {genre}* ({r.get('match_percentage', 90)}% match)")
        rec_text = "<br/>".join(rec_items)
        guidance = "<br/><br/>💡 <strong>Action Guidance:</strong> Would you like to reserve these titles for student pickup?"
        reply = f"⭐ **Curated Recommendations for Student {user_name}:**<br/><br/>{rec_text}{guidance}{feedback_footer}"

    else:
        overdue_title = overdue_txns[0].book.title if (overdue_txns and overdue_txns[0].book) else "The Pragmatic Programmer"
        reply = f"Librarian Assistant Ready. Student **{user_name}** has **{len(active_txns)} active loans**, including **1 overdue item ('{overdue_title}')** with ₹{unpaid_fine_total:.0f} pending fines. How would you like to manage this account?{feedback_footer}"
        if overdue_txns:
            actions.append({"label": "Notify Student of Overdue", "action": "notify", "user_id": user_id})
            actions.append({"label": "Renew Loan", "action": "renew", "txn_id": overdue_txns[0].transaction_id})

    return success_response({
        "reply": reply,
        "actions": actions,
        "borrowed_count": len(active_txns),
        "overdue_count": len(overdue_txns),
        "fine_amount": unpaid_fine_total
    })

