from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class User_Blog():

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_status = data['user_status']
        self.user_id = data['user_id']
        self.blog_id = data['blog_id']

    # create a new author
    @classmethod
    def create_relationship(cls, data):
        query = "INSERT INTO users_blog_status (user_status, user_id, blog_id) VALUES (%(user_status)s, %(user_id)s, %(blog_id)s);"

        new_relationship_id = connectToMySQL('blogsdb').query_db(query, data)

        return new_relationship_id

    @classmethod
    def delete_relationship(cls, data):

        query = "DELETE FROM users_blog_status WHERE id = %(id)s;"

        connectToMySQL('blogs').query_db(query, data)