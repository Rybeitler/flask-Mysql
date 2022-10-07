from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user


class Recipe:
    DB = 'recipes'

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
    
    @classmethod
    def add_new_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes =[]
        for row in results:
            recipe = cls(row)
            creator_info = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }
            creator = user.User(creator_info)
            recipe.creator = creator
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        data = {"id":recipe_id}
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        recipe = cls(results[0])
        return recipe

    @classmethod
    def delete_recipe(cls, recipe_id):
        data = {"id":recipe_id}
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s, user_id=%(user_id)s WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(recipe):
        valid = True
        loop = {
            "name":recipe["name"],
            "description":recipe["description"],
            "instructions":recipe["instructions"]
        }
        for field in recipe:
            if len(recipe[field]) <1:
                valid = False
                flash(f"{field.capitalize()} must not be blank.")
                print(f"failed {field}")
        for field in loop:
            if len(loop[field]) > 1  and len(loop[field])< 3:
                valid = False
                flash(f"{field.capitalize()} must be at least 3 characters!.")
                print(f"failed {field}")
        return valid

    