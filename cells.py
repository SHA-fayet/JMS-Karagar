from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
from .auth import login_required, admin_required

cells_bp = Blueprint('cells', __name__)

@cells_bp.route('/cells')
@login_required
def view_cells():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, COUNT(i.id) as current_occupants
        FROM cells c
        LEFT JOIN inmates i ON c.id = i.cell_id AND i.status = 'Active'
        GROUP BY c.id
        ORDER BY c.cell_number
    """)
    cells = cur.fetchall()
    cur.close()
    return render_template('cells.html', cells=cells)

@cells_bp.route('/add_cell', methods=['POST'])
@admin_required
def add_cell():
    cell_number = request.form['cell_number']
    capacity = request.form['capacity']
    
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO cells (cell_number, capacity) VALUES (%s, %s)",
        (cell_number, capacity)
    )
    mysql.connection.commit()
    cur.close()
    
    flash('Cell added successfully!', 'success')
    return redirect(url_for('cells.view_cells'))