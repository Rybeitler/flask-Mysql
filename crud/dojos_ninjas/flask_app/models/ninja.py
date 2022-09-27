from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dojo


class Ninja:
    DB = 'dojo_ninja'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_ninja(cls,data):
        query = "INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_ninja(cls, id):
        data = {"id":id}
        query = "DELETE FROM ninjas WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_dojo_id(cls, id):
        data={"id":id}
        query = "SELECT dojos.id FROM dojos left join ninjas on dojos.id=ninjas.dojo_id WHERE ninjas.id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results[0]

    @classmethod
    def get_ninja_by_id(cls, id):
        data = {'id':id}
        query = "SELECT * FROM ninjas WHERE id=%(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_ninja(cls, data):
        query = "UPDATE ninjas SET first_name=%(first_name)s,last_name=%(last_name)s, age=%(age)s WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results