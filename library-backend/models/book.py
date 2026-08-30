from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    genre = db.Column(db.String(100))
    publisher = db.Column(db.String(150))
    year = db.Column(db.SmallInteger)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    cover_image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    language = db.Column(db.String(50), default="English")
    pages = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship("Transaction", backref="book", lazy=True)
    reservations = db.relationship("Reservation", backref="book", lazy=True)
    ratings = db.relationship("BookRating", backref="book", lazy=True)

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre,
            "publisher": self.publisher,
            "year": self.year,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "cover_image_url": self.cover_image_url,
            "description": self.description,
            "language": self.language,
            "pages": self.pages,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }
