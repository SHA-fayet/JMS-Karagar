from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
from datetime import datetime
from .auth import login_required

visit_request_bp = Blueprint('visit_request', __name__)

@visit_request_bp.route('/visit_request', methods=['GET', 'POST'])
def visit_request():
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        inmate_name = request.form['inmate_name']
        date_requested = request.form.get('date_requested') or datetime.now().strftime('%Y-%m-%d')
        
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO visit_requests (visitor_name, inmate_name, date_requested) VALUES (%s, %s, %s)",
            (visitor_name, inmate_name, date_requested)
        )
        mysql.connection.commit()
        cur.close()
        
        flash('Visit request submitted!', 'success')
        return redirect(url_for('visit_request.visit_request'))
    
    return render_template('visit_request_form.html')

@visit_request_bp.route('/manage_visits')
@login_required
def manage_visits():
    if session.get('role') not in ['admin', 'jailer']:
        return "Unauthorized", 403

    import MySQLdb.cursors
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM visit_requests ORDER BY date_requested DESC")
    visits = cur.fetchall()
    cur.close()
    return render_template('manage_visits.html', visits=visits)



@visit_request_bp.route('/update_visit_status/<int:id>/<status>')
@login_required
def update_visit_status(id, status):
    if session.get('role') not in ['admin', 'jailer']:
        return "Unauthorized", 403

    if status not in ['Approved', 'Rejected']:
        flash('Invalid status!', 'danger')
        return redirect(url_for('visit_request.manage_visits'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE visit_requests SET status = %s WHERE id = %s", (status, id))
    mysql.connection.commit()
    cur.close()

    flash(f'Visit {status.lower()}!', 'success')
    return redirect(url_for('visit_request.manage_visits'))
