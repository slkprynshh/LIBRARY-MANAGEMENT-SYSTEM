from app import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum("pending", "fulfilled", "cancelled"), default="pending")
    expires_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "reserved_at": self.reserved_at.isoformat() if self.reserved_at else None,
            "status": self.status,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
