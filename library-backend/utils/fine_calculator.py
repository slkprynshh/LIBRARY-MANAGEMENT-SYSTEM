from datetime import date
from config import Config

def calculate_fine(due_date, return_date=None):
    check_date = return_date or date.today()
    if check_date > due_date:
        overdue_days = (check_date - due_date).days
        return round(overdue_days * Config.FINE_PER_DAY, 2)
    return 0.0
