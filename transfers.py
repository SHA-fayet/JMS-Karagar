from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
from datetime import datetime
from .auth import login_required, admin_required

transfers_bp = Blueprint('transfers', __name__)

@transfers_bp.route('/transfers')
@login_required
def view_transfers():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.*, i.name as inmate_name 
        FROM transfers t
        JOIN inmates i ON t.inmate_id = i.id
        ORDER BY t.transfer_date DESC
    """)
    transfers = cur.fetchall()
    
    cur.execute("SELECT id, name FROM inmates WHERE status = 'Active'")
    inmates = cur.fetchall()
    
    cur.execute("SELECT cell_number FROM cells")
    cells = cur.fetchall()
    
    cur.close()
    return render_template('transfers.html', transfers=transfers, inmates=inmates, cells=cells)

@transfers_bp.route('/add_transfer', methods=['POST'])
@admin_required
def add_transfer():
    inmate_id = request.form['inmate_id']
    from_cell = request.form['from_cell']
    to_cell = request.form['to_cell']
    transfer_date = request.form.get('transfer_date') or datetime.now().strftime('%Y-%m-%d')
    
    cur = mysql.connection.cursor()
    
    # Update inmate's cell
    cur.execute("SELECT id FROM cells WHERE cell_number = %s", (to_cell,))
    cell_id = cur.fetchone()[0]
    
    cur.execute("UPDATE inmates SET cell_id = %s WHERE id = %s", (cell_id, inmate_id))
    
    # Record transfer
    cur.execute(
        "INSERT INTO transfers (inmate_id, from_cell, to_cell, transfer_date) VALUES (%s, %s, %s, %s)",
        (inmate_id, from_cell, to_cell, transfer_date)
    )
    
    # Update cell occupancies
    cur.execute("UPDATE cells SET current_occupancy = current_occupancy - 1 WHERE cell_number = %s", (from_cell,))
    cur.execute("UPDATE cells SET current_occupancy = current_occupancy + 1 WHERE cell_number = %s", (to_cell,))
    
    mysql.connection.commit()
    cur.close()
    
    flash('Transfer recorded!', 'success')
    return redirect(url_for('transfers.view_transfers'))