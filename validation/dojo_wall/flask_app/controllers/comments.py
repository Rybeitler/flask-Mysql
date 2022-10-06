from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, comment, post

@app.route('/add-comment', methods=["POST"])
def add_comment():
    if "user_id" not in session:
        return redirect('/')
    if comment.Comment.validate_comment(request.form):
        comment.Comment.add_comment(request.form)
    return redirect("/wall")