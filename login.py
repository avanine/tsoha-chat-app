import secrets
from flask import request, session, flash
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash
from db import db


def login_user():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password, role FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user and check_password_hash(user[1], password):
        session["user_id"] = user[0]
        session["username"] = username
        session["role"] = user[2]
        session["csrf_token"] = secrets.token_hex(16)
        sql = text(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = :username"
        )
        db.session.execute(sql, {"username": username})
        db.session.commit()
        return True
    flash("Invalid username or password.", "danger")
    return False
