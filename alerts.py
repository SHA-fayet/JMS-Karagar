# app/routes/alerts.py
from flask import Blueprint
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

alerts_bp = Blueprint('alerts', __name__)

def generate_release_alerts():
    """ Dynamically imports mysql to prevent circular imports """
    from app import mysql  

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, release_date
        FROM inmates
        WHERE status = 'Active' 
        AND release_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        AND id NOT IN (SELECT inmate_id FROM alerts WHERE alert_type = 'Release' AND status = 'Active')
    """)
    upcoming = cur.fetchall()

    for inmate in upcoming:
        message = f"Inmate {inmate[1]} scheduled for release on {inmate[2]}"
        cur.execute("""
            INSERT INTO alerts (inmate_id, alert_type, alert_date, message, status)
            VALUES (%s, 'Release', %s, %s, 'Active')
        """, (inmate[0], date.today(), message))
        
        cur.execute("INSERT INTO notifications (message) VALUES (%s)", (f"New release alert: {message}, generated automatically"))

    mysql.connection.commit()
    cur.close()

# Start Scheduler **only once**
scheduler = BackgroundScheduler()
scheduler.add_job(func=generate_release_alerts, trigger="interval", hours=24)

def start_scheduler():
    """ Ensures scheduler is only started once """
    if not scheduler.running:
        scheduler.start()
