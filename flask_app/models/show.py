from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    db = "TV_DB"
    def __init__(self, data):
        self.id = data['id']
        self.added_by_id = data['added_by_id']
        self.title = data['title']
        self.network  = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.like_count = 0
        self.added_by = None
        

# create
    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO shows (added_by_id, title, network, release_date, description) VALUES(%(added_by_id)s, %(title)s,%(network)s,%(release_date)s,%(description)s);"
        return connectToMySQL(cls.db).query_db(query, form_data)

# get all
    @classmethod
    def get_all_shows(cls):
        query ="SELECT * FROM shows;"
        results = connectToMySQL(cls.db).query_db(query)
        show_list=[]
        print(results)
        for row in results:
            one_show = cls(row)
            show_list.append(one_show)
        return show_list

# get one with like count
    @classmethod
    def get_one(cls,data):
        query ="SELECT shows.*, COUNT(likes.user_id) as like_count FROM shows LEFT JOIN likes ON shows.id = likes.show_id WHERE shows.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        one_show = cls(results[0])
        one_show.like_count = results[0]['like_count']
        user_data= {'id': one_show.added_by_id}
        one_show.added_by = user.User.get_by_id(user_data)
        return one_show


# update show
    @classmethod
    def update(cls, data):
        query= "UPDATE shows SET title = %(title)s, network=%(network)s, release_date=%(release_date)s,description=%(description)s WHERE shows.id= %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
# like show
    @classmethod
    def like(cls, data):
        query= "INSERT INTO likes(user_id, show_id) VALUES(%(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
# unlike show
    @classmethod
    def unlike(cls, data):
        query= "DELETE FROM likes WHERE user_id = %(user_id)s and show_id =  %(show_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

# destroy show

    @classmethod
    def delete(cls, data):
        query= "DELETE FROM shows WHERE shows.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
# do not allow show to be added more than once
    @staticmethod
    def validate_new(show):
        is_valid = True
        query = "SELECT * FROM shows WHERE title = %(title)s;"
        results = connectToMySQL(Show.db).query_db(query,show)
        if len(results)>= 1:
            flash("Show already exists in database")
            is_valid= False
        if len(show['title']) < 1:
            flash("Title is required")
            is_valid= False
        if len(show['network'])< 1:
            flash("Network is required")
            is_valid= False
        if len(show['release_date']) < 1 :
            flash("Release Date is required")
            is_valid= False
        if len(show['description']) < 4:
            flash("Description must be atleast 3 characters")
            is_valid=False
        return is_valid

# basic validation for show
    @staticmethod
    def validate_update(show):
        is_valid = True
        if len(show['title']) < 1:
            flash("Title is required")
            is_valid= False
        if len(show['network'])< 1:
            flash("Network is required")
            is_valid= False
        if len(show['release_date']) < 1 :
            flash("Release Date is required")
            is_valid= False
        if len(show['description']) < 4:
            flash("Description must be atleast 3 characters")
            is_valid=False
        return is_valid