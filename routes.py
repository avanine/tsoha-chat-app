from flask import render_template, redirect, session
from sqlalchemy.sql import text
from app import app
import register
import login
import category
import user
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

@app.route("/login", methods=["POST"])
def login_user():
    if login.login_user():
        return redirect("/dashboard")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route('/dashboard')
def dashboard_view():
    if 'username' not in session:
        return redirect("/")
    categories = category.fetch_categories()
    users = user.fetch_all_users()
    return render_template('dashboard.html', categories=categories, users=users)

@app.route('/create-category', methods=['POST'])
def create_new_category():
    return category.create_category()
