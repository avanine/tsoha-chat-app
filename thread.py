from flask import session, request, flash, redirect, url_for
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def fetch_threads(category_id):
    threads = db.session.execute(text('''
        SELECT
            t.id,
            t.title,
            COUNT(m.id) AS message_count
        FROM
            threads t
        LEFT JOIN
            messages m ON t.id = m.thread_id
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
            id, 
            title, 
            content, 
            user_id, 
            category_id, 
            visible, 
            created_at 
        FROM threads 
        WHERE id = :thread_id
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
