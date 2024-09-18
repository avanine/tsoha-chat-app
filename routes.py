from flask import render_template
from sqlalchemy.sql import text
from app import app
from db import db

@app.route("/")
def index():
    result = db.session.execute(text("SELECT username FROM users"))
    users = result.fetchall()
    counter = len(users)
    return render_template("index.html", count=counter)
