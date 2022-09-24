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

