
from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import order


@app.route('/')
@app.route('/cookies')
def index():
    data = order.Order.get_all_orders()
    return render_template("index.html", orders=data)

@app.route('/cookies/new-order')
def new_order():
    return render_template("new-order.html")

@app.route('/cookies/place-order', methods=["POST"])
def place_order():
    if not order.Order.validate_order(request.form):
        session['name'] = request.form['name']
        session['cookie'] = request.form['cookie']
        session['boxes'] = request.form['boxes']
        return redirect('/cookies/new-order')
    session.clear()
    order.Order.add_new_order(request.form)
    return redirect('/cookies')

@app.route("/cookies/edit/<int:id>")
def edit_order(id):
    data = order.Order.get_order_by_id(id)
    print(data)
    return render_template("edit-order.html", orders=data)

@app.route("/cookies/update-order", methods=["POST"])
def update_order():
    id = request.form['id']
    if not order.Order.validate_order(request.form):
        return redirect(f'/cookies/edit/{id}')
    order.Order.update_order(request.form)
    return redirect('/cookies')