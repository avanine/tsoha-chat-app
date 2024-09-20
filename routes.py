from flask import render_template, redirect
from sqlalchemy.sql import text
from app import app
import register
from db import db

@app.route("/")
def index():
    result = db.session.execute(text("SELECT username FROM users"))
    users = result.fetchall()
    counter = len(users)
    return render_template("index.html", count=counter)

@app.route("/register", methods=["GET", "POST"])
def register_user():
    register.add_user()
    return redirect("/")
