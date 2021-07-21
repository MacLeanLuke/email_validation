from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.user_relationship_to_blog import User_Blog
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask import flash


@app.route('/blogs')
def show_all_blogs():
    # session.clear()

    if 'user' in session:
        user_data_id = {
            'id': session['user_profile_id']
        }

        all_comments_desc = []
        results = Comment.get_all_comments_desc()
        print(results)
        for item in results:
            post_data = {
                'id': item['id'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'comment_content': item['comment_content'],
                'post_id': item['post_id'],
                'user_id': item['user_id']
            }
            all_comments_desc.append(Comment(post_data))


        all_posts_desc = []
        results = Post.get_all_posts_desc()
        for item in results:
            post_data = {
                'id': item['id'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'post_content': item['post_content'],
                'blog_id': item['blog_id']
            }
            all_posts_desc.append(Post(post_data))


        # getting all users posts.
        results = Post.get_posts_by_user_id_desc(user_data_id)

        print(results)

        all_user_posts_desc = []

        for item in results:
            post_data = {
                'id': item['id'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'post_content': item['post_content'],
                'blog_id': item['blog_id']
            }
            all_user_posts_desc.append(Post(post_data))


        results = User.get_user_by_id(user_data_id)
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
        print('we got to the user')


        if len(Blog.get_blogs_by_user_id(user_data_id)) != 0:

            results = Blog.get_blogs_by_user_id(user_data_id)

            blogs = []

            for item in results:
                blog_data = {
                    'id': item['blogs.id'],
                    'created_at': item['blogs.created_at'],
                    'updated_at': item['blogs.updated_at'],
                    'name': item['name']
                }
                blogs.append(Blog(blog_data))


        else:
            blogs = ''

        print(blogs)

    else: 
        return redirect('/')

    return render_template('index.html', user=user, blogs=blogs, all_posts_desc=all_posts_desc, all_user_posts_desc=all_user_posts_desc, all_comments_desc=all_comments_desc)


@app.route('/blog/create', methods=['POST'])
def blog_create():
    if (Blog.validate_blog_create(request.form)):

        # session['user_blog'] = True

        data = {
            'name': request.form['name']
        }

        # print('we got here!!')

        session['user_blog_id'] = Blog.create_blog(data)

        print('blog create is good!')

        relationship_data = {
            'user_status': 1,
            'user_id': session['user_profile_id'],
            'blog_id': session['user_blog_id']
        }

        User_Blog.create_relationship(relationship_data)
        print('blog relationship create is good!')
    else:
        print('employee form is not good.')
        return redirect('/')
        
    return redirect('/blogs')

@app.route('/post/create', methods=['POST'])
def post_create():
    if (Post.validate_post_create(request.form)):

        # session['user_blog'] = True

        data = {
            'post_content': request.form['post_content'],
            'blog_id': request.form['blog_id']
        }

        # print('we got here!!')

        session['user_blog_post_id'] = Post.create_post(data)

        print('post create is good!')

    else:
        print('employee form is not good.')
        return redirect('/blogs')
        
    return redirect('/blogs')

@app.route('/comment/create', methods=['POST'])
def comment_create():
    if (Comment.validate_comment_create(request.form)):

        # session['user_blog'] = True

        data = {
            'comment_content': request.form['comment_content'],
            'post_id': request.form['post_id'],
            'user_id': request.form['user_id']
        }

        # print('we got here!!')

        session['user_blog_post_comment_id'] = Comment.create_comment(data)

        print('comment create is good!')

    else:
        print('comment create is not good.')
        return redirect('/blogs')
        
    return redirect('/blogs')

# @app.route('/user/login', methods=["POST"])
# def user_login():
    
#     user_in_db = User.get_users_with_email(request.form)

#     if len(user_in_db) != 1:
#         flash('Please use the sign up form to get started!')
#         return redirect('/')
        
#     user = user_in_db[0]

#     if not bcrypt.check_password_hash(user.password, request.form['password']):
#         flash("Please enter the correct password for this account.")
#         return redirect('/')

#     session['user'] = True
#     session['user_profile_id'] = user.id

#     return redirect('/users')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

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