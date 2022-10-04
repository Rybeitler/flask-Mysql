from flask_bcrypt import Bcrypt
from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models import user
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'loggedIn' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    for key in request.form:
        session[key] = request.form[key]
    if not user.User.validate_reg(request.form):
        return redirect('/')
    if user.User.check_unique_email(request.form):
        return redirect('/')
    new_user_id = user.User.add_new_user(request.form)
    new_user_name = user.User.get_users_name(new_user_id)
    session.clear()
    session['loggedIn'] = new_user_id
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    email_exists = user.User.verify_login(request.form)
    if not email_exists:
        return redirect('/')
    print("valid email")
    if not bcrypt.check_password_hash(email_exists.password, request.form['password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['loggedIn'] = email_exists.id
    session['name'] = email_exists.first_name
    return redirect('dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
