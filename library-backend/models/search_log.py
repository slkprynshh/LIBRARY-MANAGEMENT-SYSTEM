from app import db
from datetime import datetime

class SearchLog(db.Model):
    __tablename__ = "search_logs"

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    query = db.Column(db.String(255), nullable=False)
    results_count = db.Column(db.Integer, default=0)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
