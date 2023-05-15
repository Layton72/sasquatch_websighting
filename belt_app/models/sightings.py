from belt_app.config.mysqlconnection import connectToMySQL
from flask import flash, get_flashed_messages


class Sighting:
    DB = "belt_erd"
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.num_sas = data['num_sas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.num_skeptics = None

    @classmethod
    def get_all_with_user(cls):
        query = "SELECT * FROM sightings JOIN users on users.id=sightings.user_id;"
        results = connectToMySQL(cls.DB).query_db(query)
        sightings = []
        for sighting in results:
            sightings.append( cls(sighting) )
        return sightings
    
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM sightings JOIN users on users.id=sightings.user_id WHERE sightings.id = %(id)s";
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO sightings ( location, description, date, num_sas, created_at, updated_at, user_id ) VALUES ( %(location)s, %(description)s, %(date)s, %(num_sas)s, NOW() , NOW(), %(user_id)s );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data):
        query = """UPDATE sightings
                SET location=%(location)s, description=%(description)s, date=%(date)s, num_sas=%(num_sas)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if "location" not in data or len(data["location"]) == 0:
            flash("Location field is required")
            is_valid = False
        elif len(data["location"]) < 3:
            flash("Location must be at least 3 characters.")
            is_valid = False

        if "description" not in data or len(data["description"]) == 0:
            flash("Description field is required")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if "date" not in data or len(data["date"]) == 0:
            flash("Date of Sighting is required")
            is_valid = False

        if "num_sas" not in data or len(data["num_sas"]) == 0:
            flash("How many sasquatches were there?")
            is_valid = False
        elif int(data["num_sas"]) < 1:
            flash("Must report at least 1 Sasquatch")
            is_valid = False
        
        return is_valid

