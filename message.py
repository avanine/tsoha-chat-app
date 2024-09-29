import logging
from flask import session, request, flash, redirect, url_for
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_messages(thread_id):
    messages = db.session.execute(text('''
        SELECT 
            m.id, 
            m.content, 
            u.username AS creator, 
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
