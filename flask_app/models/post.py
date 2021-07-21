from typing import NewType
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Post():

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post_content = data['post_content']
        self.blog_id = data['blog_id']

    # create a new author
    @classmethod
    def create_post(cls, data):

        query = "INSERT INTO posts (post_content, blog_id) VALUES (%(post_content)s, %(blog_id)s);"

        new_post_id = connectToMySQL('blogsdb').query_db(query, data)

        return new_post_id

    @classmethod
    def delete_post(cls, data):

        query = "DELETE FROM posts WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    @classmethod
    def update_post(cls, data):

        # UPDATE table_name SET column_name1 = 'some_value', column_name2='another_value' WHERE condition(s)

        query = "UPDATE posts SET post_content = %(post_content)s WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    # return all authors
    @classmethod
    def get_all_posts_desc(cls):

        query = "SELECT * FROM posts ORDER BY created_at DESC;"

        results = connectToMySQL('blogsdb').query_db(query)

        posts = []

        for item in results:
            posts.append(item)

        print(posts)
        return posts

    @classmethod
    def get_posts_by_id(cls, data):

        query = "SELECT * FROM posts WHERE id = %(id)s;"

        result = connectToMySQL('blogsdb').query_db(query, data)

        # user = User(result[0])

        return result

    @classmethod
    def get_posts_by_user_id_desc(cls, data):

        query = "SELECT * FROM posts JOIN blogs ON posts.blog_id = blogs.id JOIN users_blog_status ON blogs.id = users_blog_status.blog_id JOIN users ON users_blog_status.user_id = users.id WHERE users.id = %(id)s ORDER BY posts.created_at DESC ;"

        results = connectToMySQL('blogsdb').query_db(query, data)

        posts = []

        for item in results:
            posts.append(item)

        return posts


    @staticmethod
    def validate_post_create(data):

        # name_regex = re.compile(r"^[A-Za-z- ']{1,255}$")
        # email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # password_regex = re.compile(r"^[a-zA-Z0-9.+_-]{8,100}$")
        # post_regex = re.compile(r"^[a-zA-Z0-9]{1,255}$")

        is_valid = True

        if len(data['post_content']) > 255 :
            flash("Your post should be less than 255 characters.")
            is_valid = False

        # if data['middle_name'] != '':
        #     if not name_regex.match(data['middle_name']):
        #         flash("Middle name should be forty-five characters or less.")
        #         is_valid = False

        # if not name_regex.match(data['last_name']):
        #     flash("Last name should be between one and one hundred characters.")
        #     is_valid = False

        # if not email_regex.match(data['email']):
        #     flash("Please stop trying to hack my database and freaking enter a valid email")
        #     is_valid = False

        # if not password_regex.match(data['password']):
        #     flash("Please enter a password with more than 10 alpha-numeric characters.")
        #     is_valid = False

        # if data['password'] != data['confirm_password']:
        #     flash('please make sure your passwords match')
        #     is_valid = False

        # if len(User.get_users_with_email({'email': data['email']})) != 0:
        #     flash('This email is already in use')
        #     is_valid = False


        # try:
        #     salary = int(data['salary'])
        #     if int(salary) < 40000 or int(salary) > 150000:
        #         flash("Salary should be between 40k and 150k.")
        #         is_valid = False

        # except:
        #     flash("Salary should be between 40k and 150k, expressed with digits.")
        #     is_valid = False

        # if data['salary'] == '':
        #     flash("Please provide a salary between 40k and 150k.")
        #     is_valid = False

        # elif int(data['salary']) < 40000 or int(data['salary']) > 150000:
        #     flash("Salary should be between 40k and 150k.")
        #     is_valid = False
        print(is_valid)
        return is_valid