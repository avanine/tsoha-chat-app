from sqlalchemy.sql import text
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
