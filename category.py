import logging
from flask import session, request, jsonify, flash, redirect, url_for
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_categories(user_id):
    categories = db.session.execute(text('''
        SELECT
            c.id AS category_id, 
            c.title AS category_name,
            COUNT(DISTINCT t.id) FILTER (WHERE t.visible = TRUE) AS thread_count,
            COUNT(m.id) FILTER (WHERE m.visible = TRUE) AS message_count,
            MAX(m.created_at) AS last_message_timestamp
        FROM 
            categories c
        LEFT JOIN 
            threads t ON c.id = t.category_id
        LEFT JOIN 
            messages m ON t.id = m.thread_id
        LEFT JOIN 
            private_categories_permissions p ON c.id = p.category_id
        WHERE
            c.visible = TRUE AND 
            (c.private = FALSE OR c.user_id = :user_id OR p.user_id = :user_id)
        GROUP BY 
            c.id, c.title
        ORDER BY 
            last_message_timestamp DESC;
    '''), {'user_id': user_id}).fetchall()

    return categories

def create_category():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Invalid input data'}), 400
    title = data.get('title')
    private = data.get('private', False)
    selected_users = data.get('users', [])
    visible = True

    if not title:
        return jsonify({'success': False, 'message': 'Title is required'}), 400

    selected_users = [user_id for user_id in selected_users if user_id]

    try:
        with db.session.begin():
            sql = text(
                "INSERT INTO categories (title, user_id, private, visible) "
                "VALUES (:title, :user_id, :private, :visible) RETURNING id"
            )
            result = db.session.execute(sql, {
                'title': title,
                'user_id': session['user_id'],
                'private': private,
                'visible': visible
            })
            category_id = result.fetchone()[0]

            if private and selected_users:
                for user_id in selected_users:
                    insert_permission_sql = text(
                        "INSERT INTO private_categories_permissions (category_id, user_id) "
                        "VALUES (:category_id, :user_id)"
                    )
                    db.session.execute(insert_permission_sql, {
                        'category_id': category_id,
                        'user_id': user_id
                    })

        db.session.commit()
        return jsonify({'success': True})

    except SQLAlchemyError as e:
        logging.error("Database error: %s", e)
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

def get_category(category_id):
    category = db.session.execute(text("SELECT * FROM categories WHERE id = :category_id"), {"category_id": category_id}).fetchone()
    if not category:
        flash("Category not found.", "danger")
        return redirect(url_for('dashboard'))
    return category

def delete_category(category_id):
    if 'username' not in session:
        return redirect("/login")
    try:
        with db.session.begin():
            sql = text("UPDATE categories SET visible = FALSE WHERE id = :category_id")
            db.session.execute(sql, {"category_id": category_id})
        db.session.commit()
        return {'success': True}
    except SQLAlchemyError as e:
        logging.error("Database error: %s", e)
        db.session.rollback()
        return {'success': False, 'message': 'An error occurred while deleting the category'}
