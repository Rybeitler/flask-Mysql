from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import dojo, ninja

@app.route('/dojos')
def home():
    all_dojos = dojo.Dojo.select_all()
    return render_template('dojos.html', dojos=all_dojos)

@app.route('/add-dojo', methods=["POST"])
def add_dojo():
    dojo.Dojo.create_dojo(request.form)
    return redirect('/dojos')

@app.route('/dojos/<int:id>')
def view_dojo(id):
    all_ninjas=dojo.Dojo.get_ninjas_from_dojo(id)
    return render_template('view_dojo.html', ninja_list = all_ninjas)