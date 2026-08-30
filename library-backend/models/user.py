from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "librarian", "student"), nullable=False)
    department = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    profile_pic = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship("Transaction", foreign_keys="Transaction.user_id", backref="student", lazy=True)
    reservations = db.relationship("Reservation", backref="user", lazy=True)
    ratings = db.relationship("BookRating", backref="user", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    fines = db.relationship("Fine", backref="user", lazy=True)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "department": self.department,
            "phone": self.phone,
            "profile_pic": self.profile_pic,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
