from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
from datetime import datetime
from .auth import login_required

work_bp = Blueprint('work', __name__)

@work_bp.route('/work_assignments')
@login_required
def view_work_assignments():
    cur = mysql.connection.cursor()
    
    # Get all work assignments with inmate names
    cur.execute("""
        SELECT w.*, i.name as inmate_name 
        FROM work_assignments w
        JOIN inmates i ON w.inmate_id = i.id
        ORDER BY w.assigned_date DESC
    """)
    assignments = cur.fetchall()
    
    # Get active inmates for dropdown
    cur.execute("SELECT id, name FROM inmates WHERE status = 'Active'")
    inmates = cur.fetchall()
    
    cur.close()
    return render_template('work_assignments.html', 
                         assignments=assignments, 
                         inmates=inmates)

@work_bp.route('/add_work_assignment', methods=['POST'])
@login_required
def add_work_assignment():
    inmate_id = request.form['inmate_id']
    work_detail = request.form['work_detail']
    supervisor = request.form.get('supervisor', '')
    assigned_date = request.form.get('assigned_date') or datetime.now().strftime('%Y-%m-%d')
    
    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO work_assignments 
        (inmate_id, work_detail, assigned_date, supervisor, status) 
        VALUES (%s, %s, %s, %s, 'Assigned')""",
        (inmate_id, work_detail, assigned_date, supervisor)
    )
    mysql.connection.commit()
    cur.close()
    
    flash('Work assignment added!', 'success')
    return redirect(url_for('work.view_work_assignments'))

@work_bp.route('/update_work_status/<int:id>', methods=['POST'])
@login_required
def update_work_status(id):
    new_status = request.form['status']
    completion_date = request.form.get('completion_date')
    
    if new_status not in ['Assigned', 'In Progress', 'Completed']:
        flash('Invalid status!', 'danger')
        return redirect(url_for('work.view_work_assignments'))
    
    cur = mysql.connection.cursor()
    
    if new_status == 'Completed' and not completion_date:
        completion_date = datetime.now().strftime('%Y-%m-%d')
    
    cur.execute(
        """UPDATE work_assignments 
        SET status = %s, completion_date = %s 
        WHERE id = %s""",
        (new_status, completion_date, id)
    )
    mysql.connection.commit()
    cur.close()
    
    flash('Work status updated!', 'success')
    return redirect(url_for('work.view_work_assignments'))

@work_bp.route('/delete_work_assignment/<int:id>')
@login_required
def delete_work_assignment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM work_assignments WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Work assignment deleted!', 'success')
    return redirect(url_for('work.view_work_assignments'))