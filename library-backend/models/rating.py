from app import db
from datetime import datetime

class BookRating(db.Model):
    __tablename__ = "book_ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    review = db.Column(db.Text, nullable=True)
    rated_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("user_id", "book_id", name="uq_user_book_rating"),)

    def to_dict(self):
        return {
            "rating_id": self.rating_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "rating": self.rating,
            "review": self.review,
            "rated_at": self.rated_at.isoformat() if self.rated_at else None,
        }
