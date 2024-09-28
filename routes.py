from flask import render_template, redirect, session
from app import app
import register
import login
import category
import user
import thread

@app.route("/")
def index():
    return render_template("index.html")

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
    categories = category.fetch_categories(session['user_id'])
    users = user.fetch_all_users()
    return render_template('dashboard.html', categories=categories, users=users)

@app.route('/create-category', methods=['POST'])
def create_new_category():
    return category.create_category()

@app.route('/category/<int:category_id>', defaults={'thread_id': None})
@app.route('/category/<int:category_id>/thread/<int:thread_id>')
def category_page(category_id, thread_id):
    selected_category = category.get_category(category_id)
    threads = thread.fetch_threads(category_id)
    if not thread_id and threads:
        selected_thread = threads[0]
    else:
        selected_thread = thread.get_thread_by_id(thread_id) if thread_id else None
    return render_template('category.html', category=selected_category, threads=threads, selected_thread=selected_thread)

@app.route('/delete-category/<int:category_id>', methods=['PATCH'])
def delete_category(category_id):
    return category.delete_category(category_id)

@app.route('/category/<int:category_id>/create-thread', methods=['POST'])
def create_thread(category_id):
    return thread.create_thread(category_id)
