from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models import User
from extensions import db
from sqlalchemy import text

def run_monthly_calculation():

    today = datetime.today()
    month = today.month - 1 or 12
    year = today.year if today.month != 1 else today.year - 1

    print(f"Running Monthly Performance for {month}/{year}")

    users = User.query.filter_by(isActive=True).all()

    for user in users:
        db.session.execute(
            text("CALL calculateMonthlyPerformance(:uid, :m, :y)"),
            {"uid": user.id, "m": month, "y": year}
        )

    db.session.commit()
    print("Monthly Performance Calculation Completed")


def start_scheduler():
    scheduler = BackgroundScheduler()


    scheduler.add_job(
        run_monthly_calculation,
        trigger='cron',
        day=1,
        hour=0,
        minute=5
    )

    scheduler.start()