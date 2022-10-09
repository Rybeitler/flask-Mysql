from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import ride, user, message

@app.route("/rides/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    rides = ride.Ride.get_ride_requests()
    rides_w_driver = ride.Ride.get_rides_w_drivers()
    return render_template("dashboard.html", logged_in_user=logged_in_user, rides=rides, rides_w_driver=rides_w_driver)

@app.route('/rides/new')
def new_ride():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template("new-ride.html", logged_in_user=logged_in_user)

@app.route('/rides/<int:id>')
def show_ride(id):
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    this_ride = ride.Ride.get_ride_by_id(id)
    messages = message.Message.get_msg_for_post(id)
    return render_template("ride-details.html", logged_in_user=logged_in_user, this_ride=this_ride, messages=messages)

@app.route('/rides/edit/<int:id>')
def edit_ride(id):
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    this_ride = ride.Ride.get_ride_by_id(id)
    return render_template("edit-ride.html", logged_in_user=logged_in_user, this_ride=this_ride)


@app.route('/rides/delete/<int:id>')
def delete_ride(id):
    ride.Ride.delete_ride(id)
    return redirect('/rides/dashboard')


@app.route('/rides/cancel/<int:id>')
def cancel_ride(id):
    ride.Ride.cancel_ride(id)
    return redirect('/rides/dashboard')

@app.route('/rides/add', methods=["POST"])
def add_ride():
    if not ride.Ride.validate_request(request.form):
        return redirect('/rides/new')
    ride.Ride.add_request(request.form)
    return redirect('/rides/dashboard')

@app.route('/rides/drive', methods=["POST"])
def drive():
    ride.Ride.drive(request.form)
    return redirect('/rides/dashboard')


@app.route('/rides/update/<int:id>', methods=["POST"])
def update_ride(id):
    if not ride.Ride.validate_request(request.form):
        return redirect(f'/rides/edit/{id}')
    ride.Ride.update_ride(request.form)
    return redirect('/rides/dashboard')