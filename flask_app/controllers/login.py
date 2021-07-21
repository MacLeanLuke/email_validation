from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/registration', methods=['POST'])
def user_registration():
    if (User.validate_user_create(request.form)):
        print('survey form is good!')
        session['user'] = True
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        # print('we got here!!')
        session['user_profile_id'] = User.create_user(data)
    else:
        print('employee form is not good.')
        return redirect('/')

    return redirect('/blogs')

@app.route('/user/login', methods=["POST"])
def user_login():
    
    user_in_db = User.get_users_with_email(request.form)

    if len(user_in_db) != 1:
        flash('Please use the sign up form to get started!')
        return redirect('/')
        
    user = user_in_db[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Please enter the correct password for this account.")
        return redirect('/')

    session['user'] = True
    session['user_profile_id'] = user.id

    return redirect('/blogs')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
