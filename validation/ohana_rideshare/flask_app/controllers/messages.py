from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, message


@app.route('/messages/post/<int:id>', methods=["POST"])
def create_message(id):
    if not message.Message.validate_msg(request.form):
        return redirect(f'/rides/{id}')
    message.Message.create_msg(request.form)
    return redirect(f'/rides/{id}')