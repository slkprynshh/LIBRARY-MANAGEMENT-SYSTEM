import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from extensions import db
import models.user, models.book, models.transaction, models.reservation
import models.fine, models.rating, models.notification, models.search_log

app = create_app()
with app.app_context():
    db.create_all()
    print("All tables created successfully.")
