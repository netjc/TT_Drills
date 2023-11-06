from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Drill:

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.steps = data['steps']
        self.user_id = data['user_id']
        self.difficulty = data['difficulty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO drills (name,description,steps,user_id,difficulty,created_at,updated_at) VALUES (%(name)s,%(description)s,%(steps)s,%(user_id)s,%(difficulty)s,Now(),Now());"
        return connectToMySQL('tt_drills').query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE drills SET name=%(name)s,description=%(description)s,steps=%(steps)s,difficulty=%(difficulty)s WHERE id = %(id)s;"
        return connectToMySQL('tt_drills').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM drills WHERE id = %(id)s;"
        return connectToMySQL('tt_drills').query_db(query,data)

    @classmethod
    def get_drill_by_id(cls,data):
        query = "SELECT * FROM drills WHERE id = %(id)s;"
        result = connectToMySQL('tt_drills').query_db(query,data)
        return cls(result[0]) 
    
    @classmethod
    def get_drills_w_creator(cls):
        query = "SELECT * FROM drills JOIN users ON drills.user_id = users.id;"
        results = connectToMySQL('tt_drills').query_db(query)
        all_drills = []
        if results:
            for row in results:
                drill = cls(row)
                data = {
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                drill.creator = user.User(data)
                all_drills.append(drill)
        return all_drills

    @classmethod
    def get_drills_w_creator_easy(cls):
        query = "SELECT * FROM drills JOIN users ON drills.user_id = users.id WHERE difficulty = 'easy';"
        results = connectToMySQL('tt_drills').query_db(query)
        all_drills = []
        if results:
            for row in results:
                drill = cls(row)
                data = {
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                drill.creator = user.User(data)
                all_drills.append(drill)
        return all_drills
    
    @classmethod
    def get_drills_w_creator_medium(cls):
        query = "SELECT * FROM drills JOIN users ON drills.user_id = users.id WHERE difficulty = 'medium';"
        results = connectToMySQL('tt_drills').query_db(query)
        all_drills = []
        if results:
            for row in results:
                drill = cls(row)
                data = {
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                drill.creator = user.User(data)
                all_drills.append(drill)
        return all_drills
    
    @classmethod
    def get_drills_w_creator_hard(cls):
        query = "SELECT * FROM drills JOIN users ON drills.user_id = users.id WHERE difficulty = 'hard';"
        results = connectToMySQL('tt_drills').query_db(query)
        all_drills = []
        if results:
            for row in results:
                drill = cls(row)
                data = {
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                drill.creator = user.User(data)
                all_drills.append(drill)
        return all_drills
    
    @classmethod
    def get_drill_w_creator(cls,data):
        print("This is your id: ",data)
        query = '''SELECT * from drills LEFT JOIN users ON drills.user_id = users.id WHERE drills.id = %(id)s;'''
        result = connectToMySQL('tt_drills').query_db(query,data)
        print(result)
        drill = cls(result[0])
        print (drill)
        data = {
                    'id':result[0]['users.id'],
                    'first_name':result[0]['first_name'],
                    'last_name':result[0]['last_name'],
                    'email':result[0]['email'],
                    'password':result[0]['password'],
                    'created_at':result[0]['users.created_at'],
                    'updated_at':result[0]['users.updated_at']
                }
        drill.creator = user.User(data)
        return drill

    @staticmethod
    def validate_drill(drill):
        is_valid = True
        if len(drill['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(drill['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(drill['steps']) < 3:
            flash("Steps must be at least 3 characters.")
            is_valid = False
        if len(drill['difficulty']) < 3:
            flash("Difficulty level has not been provided.")
            is_valid = False
        return is_valid
        
        