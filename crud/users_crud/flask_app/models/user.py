from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "users"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name'] 
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def create_user(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        results = connectToMySQL(cls.DB).query_db(query, form_data)
        return results

    @classmethod
    def get_user_by_id(cls, id):
        data = {'id':id}
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def delete_user(cls,id):
        data = {'id':id}
        query = "DELETE FROM users WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def check_unique_email(cls, user_data):
        data = {
            "email":user_data['email']
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(result)
        if len(result) == 0:
            return False
        else:
            flash("Email already in use", 'email')
            return cls(result[0])
            

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not str.isalpha(user['first_name']):
            flash("First Name cannot be blank, may only contain letters", 'first')
            is_valid = False
        if not str.isalpha(user['last_name']):
            flash("Last Name cannot be blank, may only contain letters", 'last')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", 'email')
            is_valid = False
        return is_valid