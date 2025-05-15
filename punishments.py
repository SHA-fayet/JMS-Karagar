from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import mysql
from datetime import datetime
from .auth import login_required

punishments_bp = Blueprint('punishments', __name__)

@punishments_bp.route('/punishments')
@login_required
def view_punishments():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.punishment_detail, p.date_given, i.name AS inmate_name, i.id AS inmate_id
        FROM punishments p
        JOIN inmates i ON p.inmate_id = i.id
        ORDER BY p.date_given DESC
    """)
    punishments = cur.fetchall()

    cur.execute("SELECT id, name FROM inmates WHERE status = 'Active'")
    inmates = cur.fetchall()
    cur.close()

    return render_template('punishments.html', punishments=punishments, inmates=inmates)

@punishments_bp.route('/add_punishment', methods=['POST'])
@login_required
def add_punishment():
    inmate_id = request.form['inmate_id']
    details = request.form['punishment_detail']
    date_given = request.form.get('date_given') or datetime.now().strftime('%Y-%m-%d')

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO punishments (inmate_id, punishment_detail, date_given) 
        VALUES (%s, %s, %s)
    """, (inmate_id, details, date_given))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Punishment added successfully"}), 201

@punishments_bp.route('/edit_punishment/<int:id>', methods=['POST'])
@login_required
def edit_punishment(id):
    inmate_id = request.form['inmate_id']
    details = request.form['punishment_detail']
    date_given = request.form['date_given']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE punishments 
        SET inmate_id=%s, punishment_detail=%s, date_given=%s 
        WHERE id=%s
    """, (inmate_id, details, date_given, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Punishment updated successfully"}), 200

@punishments_bp.route('/delete_punishment/<int:id>', methods=['POST'])
@login_required
def delete_punishment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM punishments WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Punishment deleted successfully"}), 200
