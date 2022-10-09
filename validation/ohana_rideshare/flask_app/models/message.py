from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Message:
    DB = 'ohana_rideshares'

    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.user_id = data["user_id"]
        self.ride_id = data["ride_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None

    @classmethod
    def create_msg(cls, data):
        query = "INSERT INTO messages (content, user_id, ride_id) VALUES (%(content)s, %(user_id)s, %(ride_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_msg_for_post(cls, id):
        data = {"id":id}
        query = "SELECT * FROM messages JOIN users on messages.user_id = users.id WHERE ride_id = %(id)s ORDER BY messages.created_at"
        results = connectToMySQL(cls.DB).query_db(query, data)
        messages = []
        for row in results:
            message = cls(row)
            message_creator = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }
            creator=user.User(message_creator)
            message.creator = creator
            messages.append(message)
        return messages

    @staticmethod
    def validate_msg(msg):
        valid = True
        if len(msg["content"]) < 1:
            valid = False
            flash("Messages cannot be blank!")
        return valid