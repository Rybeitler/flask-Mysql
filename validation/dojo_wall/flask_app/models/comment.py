from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user, post

class Comment:
    DB = "dojo_wall"

    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        self.posted_to = None

    @classmethod
    def add_comment(cls, data):
        query = "INSERT INTO comments (content, user_id, post_id) VALUES (%(content)s, %(user_id)s, %(post_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments JOIN users on comments.user_id = users.id JOIN posts ON comments.post_id = posts.id ORDER BY posts.created_at"
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        comments = []
        for row in results:
            comment = cls(row)
            comment_creator = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            posted_to = {
                "id":row["posts.id"],
                "content":row["posts.content"],
                "user_id":row["posts.user_id"],
                "created_at":row["posts.created_at"],
                "updated_at":row["posts.updated_at"]
            }
            creator=user.User(comment_creator)
            posted = post.Post(posted_to)
            comment.creator = creator
            comment.posted_to = posted
            comments.append(comment)
        return comments

    @staticmethod
    def validate_comment(data):
        valid = True
        if len(data["content"]) < 1:
            valid=False
            flash("Comments cannot be blank!", "comments")
        return valid
