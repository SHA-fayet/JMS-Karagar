# app/routes/inmates.py
from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from app import mysql
from .auth import login_required

inmates_bp = Blueprint('inmates', __name__)

# View all inmates
@inmates_bp.route('/inmates')
@login_required
def view_inmates():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.*, c.cell_number 
        FROM inmates i
        LEFT JOIN cells c ON i.cell_id = c.id
    """)
    inmates = cur.fetchall()
    cur.close()
    return render_template('inmates.html', inmates=inmates)

# Add new inmate (AJAX support added)
@inmates_bp.route('/add_inmate', methods=['POST'])
@login_required
def add_inmate():
    if session['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    
    name = request.form['name']
    crime = request.form['crime']
    sentence_duration = request.form['sentence_duration']
    admission_date = request.form['admission_date']
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO inmates 
        (name, crime, sentence_duration, admission_date, status)
        VALUES (%s, %s, %s, %s, 'Active')
    """, (name, crime, sentence_duration, admission_date))
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
    sentence_duration = request.form['sentence_duration']
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE inmates 
        SET name=%s, crime=%s, sentence_duration=%s 
        WHERE id=%s
    """, (name, crime, sentence_duration, id))
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
