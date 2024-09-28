from sqlalchemy.sql import text
from db import db

def fetch_messages(thread_id):
    messages = db.session.execute(text('''
        SELECT 
            m.id, 
            m.content, 
            u.username AS creator, 
            m.created_at 
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.thread_id = :thread_id AND m.visible = TRUE
        ORDER BY m.created_at ASC
    '''), {'thread_id': thread_id}).fetchall()
    return messages
