from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import dojo, ninja

@app.route('/ninjas/')
def ninja_page():
    all_dojos = dojo.Dojo.select_all()
    return render_template('ninjas.html', dojos=all_dojos)

@app.route('/add-ninja', methods=["POST"])
def add_ninja():
    ninja.Ninja.create_ninja(request.form)
    return redirect('/dojos')

@app.route('/ninjas/<int:id>/delete')
def delete_ninja(id):
    dojo_id = ninja.Ninja.get_dojo_id(id)
    ninja.Ninja.delete_ninja(id)
    return redirect(f"/dojos/{dojo_id['id']}")

@app.route('/ninjas/<int:id>/edit')
def edit_ninja(id):
    the_ninja = ninja.Ninja.get_ninja_by_id(id)
    return render_template("edit.html", ninja=the_ninja)

@app.route('/ninjas/update/<int:id>', methods=["POST"])
def update_ninja(id):
    dojo_id = ninja.Ninja.get_dojo_id(id)
    ninja.Ninja.update_ninja(request.form)
    return redirect(f"/dojos/{dojo_id['id']}")