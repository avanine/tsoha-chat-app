import logging
from flask import session, request, flash, redirect, url_for, jsonify, abort
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db


def fetch_messages(thread_id):
    messages = db.session.execute(
        text("""
        SELECT 
            m.id, 
            m.content, 
            u.username AS creator,
            m.user_id,
            m.created_at,
            m.last_modified
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.thread_id = :thread_id AND m.visible = TRUE
        ORDER BY m.created_at ASC
    """),
        {"thread_id": thread_id},
    ).fetchall()
    return messages


def add_message(category_id, thread_id):
    if "username" not in session:
        flash("You must be logged in to send a message.", "danger")
        return redirect(url_for("login"))

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    content = request.form.get("content")

    if not content:
        flash("Message cannot be empty.", "danger")
        return redirect(
            url_for("category_page", category_id=category_id, thread_id=thread_id)
        )
    try:
        sql = text("""
            INSERT INTO messages (content, user_id, thread_id, created_at, visible)
            VALUES (:content, :user_id, :thread_id, NOW(), TRUE)
        """)
        db.session.execute(
            sql,
            {"content": content, "user_id": session["user_id"], "thread_id": thread_id},
        )
        db.session.commit()
        flash("Message sent successfully!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error adding message: %s", e)
        flash("An error occurred while sending the message.", "danger")
    return redirect(
        url_for("category_page", category_id=category_id, thread_id=thread_id)
    )


def update_message(message_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    csrf_token = request.headers.get("X-CSRF-Token")

    if session["csrf_token"] != csrf_token:
        abort(403)

    data = request.json
    content = data.get("content")

    try:
        db.session.execute(
            text(
                "UPDATE messages SET content = :content, last_modified = NOW() WHERE id = :message_id AND user_id = :user_id"
            ),
            {
                "content": content,
                "message_id": message_id,
                "user_id": session["user_id"],
            },
        )
        db.session.commit()
        flash("Message updated successfully!", "success")
        return jsonify({"success": True})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error updating message: %s", e)
        flash("An error occurred while updating the message.", "danger")
        return jsonify({"success": False, "message": "Error updating message"})


def delete_message(message_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    csrf_token = request.headers.get("X-CSRF-Token")

    if session["csrf_token"] != csrf_token:
        abort(403)

    try:
        db.session.execute(
            text(
                "UPDATE messages SET visible = FALSE WHERE id = :message_id AND user_id = :user_id"
            ),
            {"message_id": message_id, "user_id": session["user_id"]},
        )
        db.session.commit()
        flash("Message deleted successfully!", "success")
        return jsonify({"success": True})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Error deleting message: %s", e)
        flash("An error occurred while deleting the message.", "danger")
        return jsonify({"success": False, "message": "Error deleting message"})


def search_messages():
    query = request.args.get("query")
    user_id = session.get("user_id")

    if not query:
        return jsonify([])

    sql = text("""
        SELECT 
            m.id AS message_id, 
            m.content AS message_content, 
            t.id AS thread_id, 
            t.title AS thread_title, 
            c.id AS category_id, 
            c.title AS category_title
        FROM messages m
        JOIN threads t ON m.thread_id = t.id
        JOIN categories c ON t.category_id = c.id
        LEFT JOIN private_categories_permissions p ON c.id = p.category_id
        WHERE (m.content ILIKE :query)
        AND (c.private = FALSE OR c.user_id = :user_id OR p.user_id = :user_id)
        AND m.visible = TRUE
    """)

    results = db.session.execute(
        sql, {"query": f"%{query}%", "user_id": user_id}
    ).fetchall()

    return jsonify(
        [
            {
                "message_id": row.message_id,
                "message_content": row.message_content,
                "thread_id": row.thread_id,
                "thread_title": row.thread_title,
                "category_id": row.category_id,
                "category_title": row.category_title,
            }
            for row in results
        ]
    )
