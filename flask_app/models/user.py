from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class User():

    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    # create a new author
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        new_user_id = connectToMySQL('blogsdb').query_db(query, data)

        return new_user_id

    @classmethod
    def delete_user(cls, data):

        query = "DELETE FROM users WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    @classmethod
    def update_user(cls, data):

        # UPDATE table_name SET column_name1 = 'some_value', column_name2='another_value' WHERE condition(s)

        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s   WHERE id = %(id)s;"

        connectToMySQL('blogsdb').query_db(query, data)

    # return all authors
    @classmethod
    def get_all_users(cls):

        query = "SELECT * FROM users;"

        results = connectToMySQL('blogsbd').query_db(query)

        # return results

        users = []

        for item in results:
            new_user = User(item)
            users.append(new_user)

        return users

    @classmethod
    def get_user_by_id(cls, data):

        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL('blogsdb').query_db(query, data)

        # user = User(result[0])

        return result

    @classmethod
    def get_users_with_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"

        results = connectToMySQL('blogsdb').query_db(query, data)

        users = []

        for item in results:
            users.append(User(item))

        return users


    @staticmethod
    def validate_user_create(data):

        name_regex = re.compile(r"^[A-Za-z- ']{1,100}$")
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        password_regex = re.compile(r"^[a-zA-Z0-9.+_-]{8,100}$")

        is_valid = True

        if not name_regex.match(data['first_name']):
            flash("First name should be between one and one hundred characters.")
            is_valid = False

        # if data['middle_name'] != '':
        #     if not name_regex.match(data['middle_name']):
        #         flash("Middle name should be forty-five characters or less.")
        #         is_valid = False

        if not name_regex.match(data['last_name']):
            flash("Last name should be between one and one hundred characters.")
            is_valid = False

        if not email_regex.match(data['email']):
            flash("Please stop trying to hack my database and freaking enter a valid email")
            is_valid = False

        if not password_regex.match(data['password']):
            flash("Please enter a password with 10 or more alpha-numeric characters.")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash('please make sure your passwords match')
            is_valid = False

        if len(User.get_users_with_email({'email': data['email']})) != 0:
            flash('This email is already in use')
            is_valid = False


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