from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum("issued", "returned", "overdue"), default="issued")
    fine_amount = db.Column(db.Numeric(8, 2), default=0.00)
    fine_paid = db.Column(db.Boolean, default=False)
    issued_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    fines = db.relationship("Fine", backref="transaction", lazy=True)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "issue_date": self.issue_date.isoformat() if self.issue_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "status": self.status,
            "fine_amount": float(self.fine_amount),
            "fine_paid": self.fine_paid,
            "issued_by": self.issued_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
