# app/routes/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from app import mysql
import json
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    cur = None

    try:
        cur = mysql.connection.cursor()

        # Inmate stats
        cur.execute("SELECT COUNT(*) FROM inmates WHERE status = 'Active'")
        active_inmates = cur.fetchone()
        active_inmates = active_inmates[0] if active_inmates else 0

        cur.execute("SELECT COUNT(*) FROM inmates WHERE status = 'Released'")
        released_inmates = cur.fetchone()
        released_inmates = released_inmates[0] if released_inmates else 0

        # Visitor stats
        cur.execute("SELECT COUNT(*) FROM visitors WHERE visit_date = CURDATE()")
        today_visitors = cur.fetchone()
        today_visitors = today_visitors[0] if today_visitors else 0

        # Upcoming releases
        cur.execute("""
            SELECT name, release_date 
            FROM inmates 
            WHERE release_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            AND status = 'Active'
        """)
        upcoming_releases = cur.fetchall() or []

        # Chart data
        cur.execute("""
            SELECT DATE_FORMAT(admission_date, '%Y-%m'), COUNT(*)
            FROM inmates
            GROUP BY DATE_FORMAT(admission_date, '%Y-%m')
            ORDER BY DATE_FORMAT(admission_date, '%Y-%m')
        """)
        chart_data = cur.fetchall() or []
        
        # Convert data safely for JSON rendering
        chart_labels = json.dumps([row[0] for row in chart_data])
        chart_values = json.dumps([row[1] for row in chart_data])

    finally:
        if cur:
            cur.close()

    return render_template(
        'dashboard.html',
        active_inmates=active_inmates,
        released_inmates=released_inmates,
        today_visitors=today_visitors,
        upcoming_releases=upcoming_releases,
        chart_labels=chart_labels,
        chart_values=chart_values
    )
