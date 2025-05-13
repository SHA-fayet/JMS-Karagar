# app/routes/notifications.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
from .auth import login_required, admin_required

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
@login_required
def view_notifications():
    cur = mysql.connection.cursor()
    
    # Fetch notifications
    cur.execute("SELECT * FROM notifications ORDER BY created_at DESC")
    notifications = cur.fetchall()

    # Fetch unresolved alerts and show them alongside notifications
    cur.execute("SELECT * FROM alerts WHERE status = 'Active' ORDER BY alert_date DESC")
    alerts = cur.fetchall()

    cur.close()
    return render_template('notifications.html', notifications=notifications, alerts=alerts)

@notifications_bp.route('/add_notification', methods=['POST'])
@admin_required
def add_notification():
    message = request.form['message']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notifications (message) VALUES (%s)", (message,))
    mysql.connection.commit()
    cur.close()
    
    flash('Notification added!', 'success')
    return redirect(url_for('notifications.view_notifications'))
