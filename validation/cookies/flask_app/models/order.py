
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Order:
    DB = 'cookies'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie = data['cookie']
        self.boxes = data['boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_orders(cls):
        query = "SELECT * FROM orders"
        return connectToMySQL(cls.DB).query_db(query)

    @classmethod
    def add_new_order(cls,data):
        query = "INSERT INTO orders (name, cookie, boxes) VALUES (%(name)s, %(cookie)s, %(boxes)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_order_by_id(cls,id):
        data = {"id":id}
        query = "SELECT * FROM orders WHERE id=%(id)s"
        results =  connectToMySQL(cls.DB).query_db(query, data)
        return results[0]

    @classmethod
    def update_order(cls, data):
        query = "UPDATE orders SET name=%(name)s, cookie=%(cookie)s, boxes=%(boxes)s WHERE id=%(id)s "
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @staticmethod
    def validate_order(data):
        loop_fun = {
            "name":data['name'],
            "cookie":data['cookie']
        }
        is_valid = True
        for field in loop_fun:
            if not str.isalpha(loop_fun[field]) or len(loop_fun[field]) <=0:
                is_valid = False
                flash(f"Please enter a {field}.")
                print(f"failed {field}")
        if len(data['boxes']) <=0 or int(data['boxes']) < 1:
            is_valid = False
            print("failed boxes")
            flash("Please enter a valid number of boxes.")
        return is_valid