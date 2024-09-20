from flask import request, redirect, flash
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def add_user():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    check_username = db.session.execute(text(
    "SELECT username FROM users WHERE username = :username"),
    {"username": username})
    existing_user = check_username.fetchone()

    if existing_user:
        flash('Username already in use. Please choose another one.', 'danger')
        return redirect("/")

    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect("/")

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    role = "admin" if "role" in request.form else "user"
    sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
    db.session.execute(sql, {"username":username, "password":hashed_password, "role":role})
    db.session.commit()

    return True
