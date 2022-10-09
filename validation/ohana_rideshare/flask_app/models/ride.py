from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user


class Ride:
    DB = 'ohana_rideshares'

    def __init__(self, data):
        self.id = data["id"]
        self.destination = data["destination"]
        self.pick_up = data["pick_up"]
        self.date = data["date"]
        self.details = data["details"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        self.driver = None
        self.messages = []

    @classmethod
    def add_request(cls, data):
        query = "INSERT INTO rides (destination, pick_up, date, details, user_id) VALUES (%(destination)s, %(pick_up)s, %(date)s, %(details)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_ride_requests(cls):
        query = """
                SELECT * FROM rides JOIN users ON rides.user_id = users.id
                WHERE rides.id NOT IN (SELECT ride_id FROM drivers);
                """
        results = connectToMySQL(cls.DB).query_db(query)
        rides = []
        for row in results:
            ride = cls(row)
            ride_creator = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }
            creator=user.User(ride_creator)
            ride.creator = creator
            rides.append(ride)
        return rides

    @classmethod
    def get_rides_w_drivers(cls):
        query = """
                SELECT * FROM rides JOIN users ON rides.user_id = users.id
                JOIN drivers ON rides.id = drivers.ride_id
                JOIN users AS driver ON drivers.driver_id = driver.id
                """
        results = connectToMySQL(cls.DB).query_db(query)
        rides = []
        for row in results:
            ride = cls(row)
            ride_creator = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }

            ride_driver = {
                "id":row["driver.id"],
                "first_name":row["driver.first_name"],
                "last_name":row["driver.last_name"],
                "email":row["driver.email"],
                "password":row["driver.password"],
                "created_at":row["driver.created_at"],
                "updated_at":row["driver.updated_at"]
            }
            creator=user.User(ride_creator)
            driver=user.User(ride_driver)
            ride.driver = driver
            ride.creator = creator
            rides.append(ride)
        return rides

    @classmethod
    def get_ride_by_id(cls, id):
        data = {"id":id}
        query = """
                SELECT * FROM rides JOIN users ON rides.user_id = users.id
                JOIN drivers ON rides.id = drivers.ride_id
                JOIN users AS driver ON drivers.driver_id = driver.id
                WHERE rides.id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        ride = cls(results[0])
        ride_creator = {
                "id":results[0]["users.id"],
                "first_name":results[0]["first_name"],
                "last_name":results[0]["last_name"],
                "email":results[0]["email"],
                "password":results[0]["password"],
                "created_at":results[0]["users.created_at"],
                "updated_at":results[0]["users.updated_at"]
            }
        ride_driver = {
                "id":results[0]["driver.id"],
                "first_name":results[0]["driver.first_name"],
                "last_name":results[0]["driver.last_name"],
                "email":results[0]["driver.email"],
                "password":results[0]["driver.password"],
                "created_at":results[0]["driver.created_at"],
                "updated_at":results[0]["driver.updated_at"]
            }
        creator=user.User(ride_creator)
        driver=user.User(ride_driver)
        ride.driver = driver
        ride.creator = creator
        return ride

    @classmethod
    def update_ride(cls, data):
        query = "UPDATE rides SET destination=%(destination)s, pick_up=%(pick_up)s, date=%(date)s, details=%(details)s, user_id=%(user_id)s WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def drive(cls,data):
        query = "INSERT INTO drivers (ride_id, driver_id) VALUES (%(ride_id)s, %(driver_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_ride(cls, id):
        data = {"id":id}
        query = "DELETE FROM rides WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def cancel_ride(cls, id):
        data = {"id":id}
        query = "DELETE FROM drivers WHERE ride_id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_request(request):
        valid = True
        for field in request:
            if len(request[field]) <1:
                valid = False
                flash_msg = f"{field} must not be blank.".capitalize()
                fix_msg = flash_msg.maketrans("_", " ")
                flash(flash_msg.translate(fix_msg))
        if len(request["destination"]) >=1 and len(request["destination"]) < 3:
            valid = False
            flash("Destination must be at least 3 characters.")
        if len(request["pick_up"]) >=1 and len(request["pick_up"]) < 3:
            valid = False
            flash("Location must be at least 3 characters.")
        if len(request["details"]) >=1 and len(request["details"]) < 10:
            valid = False
            flash("Details must be at least 10 characters.")
        return valid
