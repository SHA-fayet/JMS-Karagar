# app/routes/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from app import mysql
import json
from app.routes.inmates import update_released_inmates  # Import the function

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    role = session.get('role')
    cur = mysql.connection.cursor()

    # Automatically update released inmates when the dashboard is accessed
    update_released_inmates()

    # Common stats
    cur.execute("SELECT COUNT(*) FROM inmates WHERE status = 'Active'")
    active_inmates = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM inmates WHERE status = 'Released'")
    released_inmates = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM visitors WHERE visit_date = CURDATE()")
    today_visitors = cur.fetchone()[0]

    cur.execute("""
        SELECT name, release_date 
        FROM inmates 
        WHERE release_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        AND status = 'Active'
    """)
    upcoming_releases = cur.fetchall()

    #Chart
# Fetch the admission count per month for the last 2 months
    cur.execute("""
        SELECT DATE_FORMAT(admission_date, '%%Y-%%m') AS month, COUNT(*) AS count
        FROM inmates
        WHERE admission_date >= CURDATE() - INTERVAL 2 MONTH
        GROUP BY month
        ORDER BY month DESC
    """)
    chart_data = cur.fetchall()

    # Use tuple indexing instead of dict keys
    chart_labels = json.dumps([row[0] for row in chart_data])  # month
    chart_values = json.dumps([row[1] for row in chart_data])  # count


    cur.close()

    return render_template(
        'dashboard.html',
        role=role,
        active_inmates=active_inmates,
        released_inmates=released_inmates,
        today_visitors=today_visitors,
        upcoming_releases=upcoming_releases,
        chart_labels=chart_labels,
        chart_values=chart_values
    )
