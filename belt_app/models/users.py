from belt_app import app
from belt_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from datetime import date, datetime

bcrypt = Bcrypt(app)

#calculates age
def calculate_age(born):
    today = date.today()
    bday = datetime.strptime(born, "%Y-%m-%d").date()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))


#REGEXes for EMAIL AND PASSWORD
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')



class Users:
    DB = "belt_erd"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthday = data['birthday']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('belt_erd').query_db(query)

        users = []

        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name, last_name, birthday, email, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(birthday)s, %(email)s, %(password)s, NOW() , NOW() );"

        return connectToMySQL('belt_erd').query_db( query, data )


    @classmethod
    def get_one_by_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s";
        data = {'email':email}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one_by_id(cls, user_id):
        query  = "SELECT * FROM users WHERE id = %(id)s";
        data = {'id':user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        # FIRST NAME VALIDATIONS
        if "first_name" not in data or len(data["first_name"]) == 0:
            flash("First name field is required")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False

        # LAST NAME VALIDATIONS
        if "last_name" not in data or len(data["last_name"]) == 0:
            flash("Last name field is required")
            is_valid = False
        elif len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        #Birthday Validations
        if "birthday" not in data or data["birthday"] == "":
            flash("Birthdate is required")
            is_valid = False
        elif calculate_age(data["birthday"]) < 10:
            flash("Must be at least 10 years old to register")
            is_valid = False

        # EMAIL VALIDATIONS
        if "email" not in data or len(data["email"]) == 0:
            flash("Email field is required.")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        users = Users.get_all()
        for user in users:
            if data["email"] == user.email:
                flash("Email address already exists!")
                is_valid = False

        # PASSWORD VALIDATIONS
        if "password" not in data or len(data["password"]) == 0:
            flash("Password field is required.")
            is_valid = False
        elif not PASSWORD_REGEX.match(data["password"]):
            flash("Password must contain: at least 8 characters, 1 uppercase, 1 lowercase, 1 number, and 1 special character")
            is_valid = False
        elif data["confirm_password"] != data["password"]:
            flash("Passwords do not match")
            is_valid = False
        
        # TERMS AND CONDITIONS VALIDATION
        if "tc_agree" not in data:
            flash("You must agree to the Terms and Conditions")
            is_valid = False
        return is_valid
    
    # Validate the user at login
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = Users.get_one_by_email(data["email"])

        if not user_in_db:
            flash("Invalid Username or Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Invalid Username or Password")
            is_valid = False
        return is_valid

        

