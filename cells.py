# app/routes/cells.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import mysql
from .auth import login_required, admin_required
import MySQLdb.cursors

cells_bp = Blueprint('cells', __name__)

@cells_bp.route('/cells')
@login_required
def view_cells():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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

    return jsonify({'message': 'Cell added successfully'}), 201

@cells_bp.route('/edit_cell/<int:id>', methods=['POST'])
@admin_required
def edit_cell(id):
    cell_number = request.form['cell_number']
    capacity = request.form['capacity']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE cells 
        SET cell_number=%s, capacity=%s 
        WHERE id=%s
    """, (cell_number, capacity, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Cell updated successfully'}), 200

@cells_bp.route('/assign_cell', methods=['GET', 'POST'])
@login_required
def assign_cell():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        if session['role'] not in ['admin', 'jailer']:
            return jsonify({"error": "Unauthorized access"}), 403

        inmate_id = request.form['inmate_id']
        cell_id = request.form['cell_id']

        # Check cell capacity
        cur.execute("SELECT capacity, current_occupancy FROM cells WHERE id = %s", (cell_id,))
        cell = cur.fetchone()
        if not cell or cell['current_occupancy'] >= cell['capacity']:
            return jsonify({"error": "Cell is full or invalid"}), 400

        # Update inmate and cell occupancy
        cur.execute("UPDATE inmates SET cell_id=%s WHERE id=%s", (cell_id, inmate_id))
        cur.execute("UPDATE cells SET current_occupancy = current_occupancy + 1 WHERE id=%s", (cell_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Cell assigned successfully"})

    # GET: Render page with data
    cur.execute("SELECT id, name FROM inmates WHERE cell_id IS NULL AND status = 'Active'")
    unassigned_inmates = cur.fetchall()

    cur.execute("SELECT * FROM cells WHERE current_occupancy < capacity")
    available_cells = cur.fetchall()
    cur.close()

    return render_template('assign_cell.html', unassigned_inmates=unassigned_inmates, available_cells=available_cells)

