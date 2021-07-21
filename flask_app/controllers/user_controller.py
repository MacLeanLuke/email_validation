from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.user_model import User
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def show_all_users():
    # session.clear()
    if 'user' in session:
        data = {
            'id': session['user_profile_id']
        }
        results = User.get_user_by_id(data)
        # print(results)
        user_data = {
            'id': results[0]['id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password']
        }
        user = User(user_data)

    return render_template('index.html', user=user)


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
    return redirect('/users')

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

    return redirect('/users')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# @app.route('/user')
# def user_profile():
#     if 'user_profile' in session:
#         data = {
#             'id': session['user_profile']
#         }
#         results = User.get_user_by_id(data)
#         user_data = {
#             'id': results[0]['id'],
#             'created_at': results[0]['created_at'],
#             'updated_at': results[0]['updated_at'],
#             'first_name': results[0]['first_name'],
#             'last_name': results[0]['last_name'],
#             'email': results[0]['email']
#         }
#         user = User(user_data)
        
        
#     return render_template('generic.html', user=user)




# from flask_app.models.user import User
# @app.route('/register', methods=['POST'])
# def register():
#     if not User.validate_user(request.form):
#         # we redirect to the template with the form.
#         return redirect('/')
#     # ... do other things
#     return redirect('/dashboard')