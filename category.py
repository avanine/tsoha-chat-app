from flask import session, request, jsonify
from sqlalchemy.sql import text
from db import db

def fetch_categories():
    categories = db.session.execute(text('''
        SELECT
            c.id AS category_id, 
            c.title AS category_name,
            COUNT(DISTINCT t.id) AS thread_count,
            COUNT(m.id) AS message_count,
            MAX(m.created_at) AS last_message_timestamp
        FROM 
            categories c
        LEFT JOIN 
            threads t ON c.id = t.category_id
        LEFT JOIN 
            messages m ON t.id = m.thread_id
        WHERE
            c.visible = TRUE
        GROUP BY 
            c.id, c.title
        ORDER BY 
            last_message_timestamp DESC;
    ''')).fetchall()

    return categories

def create_category():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Invalid input data'}), 400
    title = data.get('title')
    private = data.get('private', False)
    visible = True

    if not title:
        return jsonify({'success': False, 'message': 'Title is required'}), 400

    sql = text(
        "INSERT INTO categories (title, user_id, private, visible) VALUES (:title, :user_id, :private, :visible)")
    db.session.execute(sql, {
        'title': title,
        'user_id': session['user_id'],
        'private': private,
        'visible': visible
    })
    db.session.commit()

    return jsonify({'success': True})
