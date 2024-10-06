import logging
from flask import session, request, flash, redirect, url_for, jsonify
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_threads(category_id):
    threads = db.session.execute(text('''
        SELECT
            t.id,
            t.title,
            t.user_id,
            COUNT(m.id) AS message_count
        FROM
            threads t
        LEFT JOIN
            messages m ON t.id = m.thread_id AND m.visible = TRUE
        WHERE
            t.category_id = :category_id AND t.visible = TRUE
        GROUP BY
            t.id
        ORDER BY
            MAX(m.created_at) DESC;
    '''), {'category_id': category_id}).fetchall()
    return threads

def get_thread_by_id(thread_id):
    thread = db.session.execute(text('''
        SELECT 
            t.id, 
            t.title, 
            t.content, 
            t.created_at,
            t.last_modified,
            t.user_id,
            u.username AS creator
        FROM threads t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = :thread_id
    '''), {"thread_id": thread_id}).fetchone()
    return thread

def create_thread(category_id):
    if 'username' not in session:
        return redirect("/login")

    title = request.form.get('title')
    content = request.form.get('content')
    user_id = session['user_id']

    if not title or not content:
        flash("Title and content are required to create a thread.", "danger")
        return redirect(url_for('category_page', category_id=category_id))

    try:
        sql = text('''
            INSERT INTO threads (title, content, user_id, category_id, visible, created_at)
            VALUES (:title, :content, :user_id, :category_id, TRUE, NOW())
            RETURNING id;
        ''')
        result = db.session.execute(sql, {
            'title': title,
            'content': content,
            'user_id': user_id,
            'category_id': category_id
        })
        db.session.commit()
        thread_id = result.fetchone()[0]

    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while creating the thread.", "danger")
        return redirect(url_for('category_page', category_id=category_id))

    if thread_id:
        flash("Thread created successfully!", "success")
        return redirect(url_for('category_page', category_id=category_id, thread_id=thread_id))

    flash("Error creating the thread.", "danger")
    return redirect(url_for('category_page', category_id=category_id))

def delete_thread(thread_id):
    if 'username' not in session:
        return redirect("/login")
    try:
        sql = text('UPDATE threads SET visible = FALSE WHERE id = :thread_id')
        db.session.execute(sql, {'thread_id': thread_id})
        db.session.commit()
        flash("Thread deleted successfully.", "success")
        return {'success': True}
    except SQLAlchemyError as e:
        logging.error("Database error: %s", e)
        db.session.rollback()
        flash("You are not authorized to delete this thread.", "danger")
        return {'success': False, 'message': 'An error occurred while deleting the thread'}

def update_thread(thread_id):
    if 'username' not in session:
        return redirect("/login")

    thread_to_update = get_thread_by_id(thread_id)

    if thread_to_update and thread_to_update.user_id == session['user_id']:
        data = request.json
        new_title = data.get('title')
        new_content = data.get('content')

        try:
            sql = text('UPDATE threads SET title = :title, content = :content, last_modified = NOW() WHERE id = :thread_id')
            db.session.execute(sql, {'title': new_title, 'content': new_content, 'thread_id': thread_id})
            db.session.commit()
            flash("Thread updated successfully.", "success")
            return jsonify({'success': True})
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("Database error: %s", e)
            return jsonify({'success': False, 'message': 'An error occurred while updating the thread'}), 500
    else:
        return jsonify({'success': False, 'message': 'You are not authorized to edit this thread'}), 403
