from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")
DATE_REGEX = re.compile("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$")
bcrypt = Bcrypt(app)

class User:
    DB = 'login_reg'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.DOB = data['DOB']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_new_user(cls, user_info):
        pw_hash = bcrypt.generate_password_hash(user_info['password'])
        data = {
            "first_name":user_info['first_name'],
            "last_name":user_info['last_name'],
            "email":user_info['email'],
            "password":pw_hash,
            "DOB":user_info['DOB']
        }
        print(data)
        query = "INSERT INTO users (first_name, last_name, email, password, DOB) Values (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(DOB)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def check_unique_email(cls, user_data):
        data = {
            "email":user_data['email']
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) == 0:
            return False
        else:
            flash("Email already in use", 'email')
            return cls(result[0])

    @classmethod
    def get_users_name(cls,id):
        data = {'id':id}
        query = "SELECT first_name FROM users WHERE users.id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def verify_login(cls, user_info):
        data = {'email': user_info['email'],
        }
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(len(results))
        if len(results) == 0:
            flash("Invalid email/password.", 'login')
            return False
        else:
            return cls(results[0])


    @staticmethod
    def validate_reg(data):
        loop_data = {
            "first_name":data['first_name'],
            "last_name":data['last_name']
        }
        is_valid = True
        for field in loop_data:
            if not str.isalpha(loop_data[field]) or len(loop_data[field]) < 2:
                is_valid = False
                message = f"Please enter a valid {field}."
                make_pretty = message.maketrans("_", " ")
                flash(message.translate(make_pretty), 'name')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Please enter a valid email address.", 'email')
        if not PW_REGEX.match(data['password']):
            is_valid = False
            flash("Passwords must be at least 8 characters and contain one capital and one number", 'password')
        if not data['password'] == data['confirm_pw']:
            is_valid = False
            flash("Please confirm passwords match", 'password')
        return is_valid
