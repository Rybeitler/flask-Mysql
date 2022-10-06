from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, comment, post



@app.route("/wall")
def wall():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    all_posts = post.Post.get_all_posts()
    all_comments = comment.Comment.get_all_comments()
    print(all_posts)
    return render_template("/wall.html", logged_in_user=logged_in_user, posts = all_posts, comments = all_comments)

@app.route('/add-post', methods=["POST"])
def add_post():
    if "user_id" not in session:
        return redirect('/')
    if post.Post.validate_post(request.form):
        post.Post.add_post(request.form)
    return redirect("/wall")

@app.route('/delete-post/<int:id>')
def delete_post(id):
    post.Post.delete_post(id)
    return redirect("/wall")