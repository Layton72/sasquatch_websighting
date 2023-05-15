from belt_app.config.mysqlconnection import connectToMySQL



class Skeptic:
    DB = "belt_erd"
    def __init__( self , data ):
        self.user_id = data['users.id']
        self.sighting_id = data['sighting_id']
        self.first_name = data['first_name']

    @classmethod
    def get_all_skeptics(cls, sighting_id):
        query = """SELECT * FROM sightings 
        JOIN skeptics ON skeptics.sighting_id=sightings.id 
        JOIN users ON users.id=skeptics.user_id
        WHERE sightings.id = %(id)s;"""
        data = {
            'id': sighting_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        skeptics = []
        for skeptic in results:
            skeptics.append( cls(skeptic) )
        return skeptics
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO skeptics ( user_id, sighting_id ) VALUES (%(user_id)s, %(sighting_id)s );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM skeptics WHERE skeptics.user_id = %(user_id)s AND skeptics.sighting_id = %(sighting_id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)