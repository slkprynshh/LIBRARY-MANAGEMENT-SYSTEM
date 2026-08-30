from extensions import db
from models.notification import Notification

def send_notification(user_id, message, notif_type="general"):
    notif = Notification(user_id=user_id, message=message, type=notif_type)
    db.session.add(notif)
    db.session.commit()
