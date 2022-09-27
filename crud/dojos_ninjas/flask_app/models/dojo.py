from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dojo
class Dojo:
    DB = "dojo_ninja"
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas =[]

    @classmethod
    def create_dojo(cls,data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def select_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL(cls.DB).query_db(query)
        dojos = []
        for row in results:
            dojos.append(cls(row))
        return dojos

    @classmethod
    def get_ninjas_from_dojo(cls, id):
        data = {'id':id}
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        dojo = cls(results[0])
        print(results)
        for row in results:
            ninja_data={
                "id":row['ninjas.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "age":row['age'],
                "created_at":row['ninjas.created_at'],
                "updated_at":row['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(ninja_data))
        return dojo


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

