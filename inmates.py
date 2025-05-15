# app/routes/inmates.py

from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from app import mysql
from .auth import login_required
import MySQLdb.cursors
from datetime import date

inmates_bp = Blueprint('inmates', __name__)

# View all inmates
@inmates_bp.route('/inmates')
@login_required
def view_inmates():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor here!
    cur.execute("""
        SELECT i.*, c.cell_number 
        FROM inmates i
        LEFT JOIN cells c ON i.cell_id = c.id
    """)
    inmates = cur.fetchall()
    cur.close()
    return render_template('inmates.html', inmates=inmates)

def update_released_inmates():
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE inmates 
        SET status = 'Released'
        WHERE status = 'Active' AND release_date < %s
    """, (date.today(),))
    mysql.connection.commit()
    cur.close()

    
# Add new inmate
@inmates_bp.route('/add_inmate', methods=['POST'])
@login_required
def add_inmate():
    if session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    name = request.form['name']
    crime = request.form['crime']
    sentence = request.form['sentence']  # <- Fix: get 'sentence'
    sentence_duration = request.form['sentence_duration']
    admission_date = request.form['admission_date']
    release_date = request.form['release_date']

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO inmates 
        (name, crime, sentence, sentence_duration, admission_date, release_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Active')
    """, (name, crime, sentence, sentence_duration, admission_date, release_date))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Inmate added successfully"}), 201

# Edit inmate
@inmates_bp.route('/edit_inmate/<int:id>', methods=['POST'])
@login_required
def edit_inmate(id):
    if session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    name = request.form['name']
    crime = request.form['crime']
    sentence = request.form['sentence']  # <- Fix: get 'sentence'
    sentence_duration = request.form['sentence_duration']
    release_date = request.form['release_date']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE inmates 
        SET name=%s, crime=%s, sentence=%s, sentence_duration=%s, release_date=%s
        WHERE id=%s
    """, (name, crime, sentence, sentence_duration, release_date, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Inmate updated successfully"}), 200


# Delete inmate
@inmates_bp.route('/delete_inmate/<int:id>', methods=['POST'])
@login_required
def delete_inmate(id):
    if session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inmates WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Inmate deleted successfully"}), 200
