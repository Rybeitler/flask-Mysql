from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Post:
    DB = 'dojo_wall'

    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None

    @classmethod
    def add_post(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users on posts.user_id = users.id ORDER BY posts.created_at"
        results = connectToMySQL(cls.DB).query_db(query)
        posts = []
        for row in results:
            post = cls(row)
            post_creator = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }
            creator=user.User(post_creator)
            post.creator = creator
            posts.append(post)
        return posts

    @classmethod
    def delete_post(cls, id):
        data = {
            "id":id
        }
        query = "DELETE FROM posts WHERE posts.id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_post(data):
        valid = True
        if len(data["content"]) < 1:
            valid=False
            flash("Posts cannot be blank!", "posts")
        return valid

    