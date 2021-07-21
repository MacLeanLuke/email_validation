from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Blog():

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']

    # create a new author
    @classmethod
    def create_blog(cls, data):
        query = "INSERT INTO blogs (name) VALUES (%(name)s);"

        new_blog_id = connectToMySQL('blogsdb').query_db(query, data)

        return new_blog_id

    @classmethod
    def delete_blog(cls, data):

        query = "DELETE FROM blogs WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    @classmethod
    def update_blog(cls, data):

        # UPDATE table_name SET column_name1 = 'some_value', column_name2='another_value' WHERE condition(s)

        query = "UPDATE blogs SET name = %(name)s WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    # return all authors
    @classmethod
    def get_all_blogs(cls):

        query = "SELECT * FROM blogs;"

        results = connectToMySQL('blogsbd').query_db(query)

        # return results

        blogs = []

        for item in results:
            new_blog = Blog(item)
            blogs.append(new_blog)

        return blogs

    @classmethod
    def get_blog_by_id(cls, data):

        query = "SELECT * FROM blogs WHERE id = %(id)s;"

        result = connectToMySQL('blogsdb').query_db(query, data)

        # user = User(result[0])

        return result

    # @classmethod
    # def get_all_blogs_except_id(cls, data):

    #     qu

    @classmethod
    def get_blogs_by_user_id(cls, data):

        query = "SELECT * FROM users JOIN users_blog_status ON users.id = users_blog_status.user_id JOIN blogs ON users_blog_status.blog_id = blogs.id WHERE users.id = %(id)s;"

        results = connectToMySQL('blogsdb').query_db(query, data)

        blogs = []

        for item in results:
            blogs.append(item)

        print(blogs)
        return blogs

    # @classmethod
    # def get_all_blogs_except_id(cls, data):

    #     query = "SELECT * FROM users JOIN users_blog_status ON users.id = users_blog_status.user_id JOIN blogs ON users_blog_status.blog_id = blogs.id WHERE users.id != %(id)s;"

    #     results = connectToMySQL('blogsdb').query_db(query, data)

    #     blogs = []

    #     for item in results:
    #         blogs.append(item)

    #     print(blogs)
    #     return blogs


    @staticmethod
    def validate_blog_create(data):

        name_regex = re.compile(r"^[A-Za-z- ']{1,45}$")
        # email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # password_regex = re.compile(r"^[a-zA-Z0-9.+_-]{8,100}$")

        is_valid = True

        if not name_regex.match(data['name']):
            flash("First name should be between one and forty-five.")
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