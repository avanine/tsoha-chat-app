import logging
from flask import session, request, flash, redirect, url_for, jsonify
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_messages(thread_id):
    messages = db.session.execute(text('''
        SELECT 
            m.id, 
            m.content, 
            u.username AS creator,
            m.user_id,
            m.created_at,
            m.last_modified
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.thread_id = :thread_id AND m.visible = TRUE
        ORDER BY m.created_at ASC
    '''), {'thread_id': thread_id}).fetchall()
    return messages

def add_message(category_id, thread_id):
    content = request.form.get('content')
    if 'username' not in session:
        flash("You must be logged in to send a message.", "danger")
        return redirect(url_for('login'))
    if not content:
        flash("Message cannot be empty.", "danger")
        return redirect(url_for('category_page', category_id=category_id, thread_id=thread_id))
    try:
        sql = text("""
            INSERT INTO messages (content, user_id, thread_id, created_at, visible)
            VALUES (:content, :user_id, :thread_id, NOW(), TRUE)
        """)
        db.session.execute(sql, {
            'content': content,
            'user_id': session['user_id'],
            'thread_id': thread_id
        })
        db.session.commit()
        flash("Message sent successfully!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error adding message: %s", e)
        flash("An error occurred while sending the message.", "danger")
    return redirect(url_for('category_page', category_id=category_id, thread_id=thread_id))

def update_message(message_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.json
    content = data.get('content')

    try:
        db.session.execute(text("UPDATE messages SET content = :content, last_modified = NOW() WHERE id = :message_id AND user_id = :user_id"),
                           {'content': content, 'message_id': message_id, 'user_id': session['user_id']})
        db.session.commit()
        return jsonify({'success': True})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error updating message: %s", e)
        flash("An error occurred while updating the message.", "danger")
        return jsonify({'success': False, 'message': 'Error updating message'})

def delete_message(message_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        db.session.execute(text("UPDATE messages SET visible = FALSE WHERE id = :message_id AND user_id = :user_id"),
                           {'message_id': message_id, 'user_id': session['user_id']})
        db.session.commit()
        return jsonify({'success': True})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error deleting message: %s", e)
        flash("An error occurred while deleting the message.", "danger")
        return jsonify({'success': False, 'message': 'Error deleting message'})
