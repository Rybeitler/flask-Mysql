from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")

class User:
    DB = 'recipes'

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def register(cls, user_data):
        data = {
            "first_name":user_data["first_name"],
            "last_name":user_data["last_name"],
            "email":user_data["email"],
            "password":bcrypt.generate_password_hash(user_data["password"])
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {
            "id":id
            }
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(f"{result} id")
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls, email):
        data = {
            "email":email
            }
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(f"{result} email")
        if len(result) ==0:
            return False
        else:
            return cls(result[0])

    @staticmethod
    def validate_user(user):
        valid = True
        email_in_db = User.get_user_by_email(user["email"])
        if len(user["first_name"]) < 2:
            flash("First name needs to be at least 2 characters", "name")
            valid = False
        if len(user["last_name"]) < 2:
            flash("Last name needs to be at least 2 characters", "name")
            valid = False
        if not EMAIL_REGEX.match(user['email']):
            valid = False
            flash("Please enter a valid email", "email")
        if email_in_db is not False:
            valid = False
            flash("Email already in use!", "email")
        if not PW_REGEX.match(user["password"]):
            valid = False
            flash("Passwords must be at least 8 characters and contain one capital and one number", "password")
        if user["password"] != user["confirm_pw"]:
            valid = False
            flash("Please be sure to confirm passwords match", "password")
        return valid

    @staticmethod
    def validate_login(user):
        valid = True
        email_in_db = User.get_user_by_email(user["email"])
        print("email in db", email_in_db)
        if not EMAIL_REGEX.match(user["email"]):
            valid = False
            flash("Please enter a vaild email", "login")
        if email_in_db is False:
            valid = False
            flash("Incorrect email/password combination", "login")
        else:
            if len(user["password"]) < 8 or not bcrypt.check_password_hash(email_in_db.password, user["password"]):
                valid = False
                flash("Incorrect email/password combination", "login")
        if valid:
            return email_in_db
        else:
            return valid
