from flask import Blueprint, request
from extensions import db
from models.book import Book
from models.transaction import Transaction
from models.search_log import SearchLog
from utils.auth_helpers import success_response, error_response, token_required, role_required
from ai.nlp_search import NLPSearch
from sqlalchemy import func

books_bp = Blueprint("books", __name__)
nlp_search = NLPSearch()

@books_bp.route("", methods=["GET"])
def get_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    genre = request.args.get("genre")
    author = request.args.get("author")
    available = request.args.get("available")

    query = Book.query
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if available == "true":
        query = query.filter(Book.available_copies > 0)

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return success_response({
        "books": [b.to_dict() for b in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": page,
    })

@books_bp.route("/search", methods=["GET"])
def search_books():
    q = request.args.get("q", "").strip()
    if not q:
        return error_response("Query parameter 'q' is required", 400)
    books = Book.query.all()
    results = nlp_search.search(q, books)
    user_id = None
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]
        from utils.auth_helpers import decode_token
        user_id = decode_token(token).get("user_id")
    except Exception:
        pass
    log = SearchLog(user_id=user_id, query=q, results_count=len(results))
    db.session.add(log)
    db.session.commit()
    return success_response({"results": results, "count": len(results)})

@books_bp.route("/genres", methods=["GET"])
def get_genres():
    genres = db.session.query(Book.genre).distinct().filter(Book.genre.isnot(None)).all()
    return success_response({"genres": [g[0] for g in genres]})

@books_bp.route("/popular", methods=["GET"])
def popular_books():
    results = (
        db.session.query(Book, func.count(Transaction.transaction_id).label("borrow_count"))
        .join(Transaction, Transaction.book_id == Book.book_id)
        .group_by(Book.book_id)
        .order_by(func.count(Transaction.transaction_id).desc())
        .limit(10)
        .all()
    )
    data = [{**b.to_dict(), "borrow_count": count} for b, count in results]
    return success_response({"books": data})

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return success_response(book.to_dict())

@books_bp.route("", methods=["POST"])
@role_required("admin", "librarian")
def add_book():
    data = request.get_json()
    if not data.get("title") or not data.get("author"):
        return error_response("title and author are required", 400)
    book = Book(
        title=data["title"], author=data["author"],
        isbn=data.get("isbn"), genre=data.get("genre"),
        publisher=data.get("publisher"), year=data.get("year"),
        total_copies=data.get("total_copies", 1),
        available_copies=data.get("total_copies", 1),
        cover_image_url=data.get("cover_image_url"),
        description=data.get("description"),
        language=data.get("language", "English"),
        pages=data.get("pages"),
    )
    db.session.add(book)
    db.session.commit()
    nlp_search.rebuild_index()
    return success_response(book.to_dict(), "Book added successfully", 201)

@books_bp.route("/<int:book_id>", methods=["PUT"])
@role_required("admin", "librarian")
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    for field in ["title", "author", "isbn", "genre", "publisher", "year",
                  "total_copies", "available_copies", "cover_image_url",
                  "description", "language", "pages"]:
        if field in data:
            setattr(book, field, data[field])
    db.session.commit()
    nlp_search.rebuild_index()
    return success_response(book.to_dict(), "Book updated successfully")

@books_bp.route("/<int:book_id>", methods=["DELETE"])
@role_required("admin")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return success_response(message="Book deleted successfully")
