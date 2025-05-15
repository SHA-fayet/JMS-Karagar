from flask import Blueprint, render_template, request, redirect, session, flash
from app import mysql
from .auth import login_required

visitors_bp = Blueprint('visitors', __name__)

@visitors_bp.route('/visitors')
@login_required
def view_visitors():
    cur = mysql.connection.cursor()
    
    # Visitor list with inmate names
    cur.execute("""
        SELECT v.*, i.name AS inmate_name 
        FROM visitors v
        JOIN inmates i ON v.inmate_id = i.id
        ORDER BY visit_date DESC
    """)
    visitors = cur.fetchall()
    
    # Fetch active inmates for dropdown
    cur.execute("SELECT id, name FROM inmates WHERE status = 'Active'")
    inmates = cur.fetchall()
    
    cur.close()
    return render_template('visitors.html', visitors=visitors, inmates=inmates)

@visitors_bp.route('/add_visitor', methods=['POST'])
@login_required
def add_visitor():
    inmate_id = request.form['inmate_id']
    visitor_name = request.form['visitor_name']
    relation = request.form['relation']
    visit_date = request.form['visit_date']
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO visitors 
        (inmate_id, visitor_name, relation, visit_date)
        VALUES (%s, %s, %s, %s)
    """, (inmate_id, visitor_name, relation, visit_date))
    mysql.connection.commit()
    cur.close()
    
    flash('Visitor added successfully', 'success')
    return redirect('/visitors')
