from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import drill
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w\d!@#$%^&*]")

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.drills = []

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if not str.isalpha(user['first_name']):
            flash("First Name must consist of letters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not str.isalpha(user['last_name']):
            flash("Last Name must only consist of letters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address format")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not PW_REGEX.match(user['password']): 
            flash("Password must contain at least one special character: !,@,#,$,%,^,&,*")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL('tt_drills').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users
    
    @classmethod
    def save(cls,data): 
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, Now(), Now());"
        return connectToMySQL('tt_drills').query_db(query, data)  
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s,last_name = %(last_name)s, email = %(email)s, updated_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("tt_drills").query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('tt_drills').query_db(query,data)

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('tt_drills').query_db(query,data)
        print("one user:", result)
        return cls(result[0])
    
    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('tt_drills').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_users_w_drills(cls):
        query = "SELECT * FROM users JOIN drills ON users.id = drills.user_id"
        results = connectToMySQL('user-test').query_db(query)
        if results:
            new_result = []
            for row in results:
                user = cls(row)
                data = {
                    "id":row['drills.id'],
                    "name":row['name'],
                    "description":row['description'],
                    "instructions":row['instructions'],
                    'user_id':row['user_id'],
                    "created_at":row['drills.created_at'],
                    "updated_at":row['drills.updated_at']
                }
                user.drills.append(drill.Drill(data))
                new_result.append(user)
            return new_result
