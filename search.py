from flask import Blueprint, render_template, request
from app import mysql
from .auth import login_required

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'inmates')
    results = []
    
    if query:
        cur = mysql.connection.cursor()
        
        if category == 'inmates':
            cur.execute("SELECT * FROM inmates WHERE name LIKE %s", (f'%{query}%',))
            results = cur.fetchall()
            
        elif category == 'visitors':
            cur.execute("SELECT * FROM visitors WHERE visitor_name LIKE %s", (f'%{query}%',))
            results = cur.fetchall()
            
        elif category == 'cells':
            cur.execute("SELECT * FROM cells WHERE cell_number LIKE %s", (f'%{query}%',))
            results = cur.fetchall()
            
        cur.close()
    
    return render_template('search.html', results=results, query=query, category=category)