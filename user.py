from sqlalchemy.sql import text
from db import db

def fetch_all_users():
    users = db.session.execute(text('''
        SELECT
            u.id AS user_id, 
            u.username AS username
        FROM 
            users u
        ORDER BY 
            u.username ASC;
    ''')).fetchall()

    return users
