from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

from flask import flash

class Anime:
    db = "anime_reviews"
    def __init__(self, data):
        self.id = data['id'] 
        self.name = data['name']
        self.review = data['review']
        self.rating = data['rating']
        self.watch_date = data['watch_date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        
    @classmethod
    def get_all_animes(cls):
        query = "SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        animes = []
        for row in results:
            anime = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            anime.user = user.User(user_data)
            animes.append(anime)
        return animes
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO animes (name, review, rating, watch_date, user_id) VALUES (%(name)s, %(review)s, %(rating)s, %(watch_date)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE animes SET name=%(name)s, review=%(review)s, rating=%(rating)s, watch_date=%(watch_date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM animes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    
    @classmethod
    def get_by_anime_id(cls,data):
        query = "SELECT * FROM animes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_anime(anime):
        is_valid = True
        if len(anime['name']) < 3:
            flash('anime name must be at least 3 characters', 'create')
            is_valid = False
        if len(anime['review']) < 3:
            flash('anime review must include at least 3 characters', 'create')
            is_valid = False
        if anime['watch_date'] == '':
            flash('Please enter a date','create')
            is_valid = False
        return is_valid