from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user

@app.route("/")
def index():
    users = user.User.get_all_users()
    return render_template("read.html", users = users)

@app.route("/create-user")
def create_user():
    return render_template('create.html')

@app.route("/add-user", methods=["POST"])
def add_product():
    print(request.form)
    user.User.create_user(request.form)
    return redirect("/")

@app.route('/get-user/<id>')
def get_user(id):
    the_user = user.User.get_user_by_id(id)
    return render_template("read_one.html", user = the_user)

@app.route('/get-user/<id>/delete')
def delete_user(id):
    user.User.delete_user(id)
    return redirect('/')

@app.route('/get-user/<id>/edit')
def edit_user(id):
    the_user = user.User.get_user_by_id(id)
    return render_template("edit.html", user = the_user)

@app.route('/update-user', methods=["POST"])
def update_user():
    user.User.update_user(request.form)
    return redirect('/')