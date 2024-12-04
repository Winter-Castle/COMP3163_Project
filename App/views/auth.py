# from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_jwt_extended import unset_access_cookies, create_access_token, set_access_cookies
# from flask_login import current_user
# from App.models import User
# from App.controllers import (create_user, jwt_authenticate, login, 
#   get_all_users, get_all_users_json, create_staff, login_user)

# auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
# '''
# Page/Action Routes
# '''


# @auth_views.route('/users', methods=['GET'])
# def get_user_page():
#   users = get_all_users()
#   return render_template('users.html', users=users)


# @auth_views.route('/identify', methods=['GET'])
# @jwt_required()
# def identify_page():
#   return jsonify({
#       'message':
#       f"username: {current_user.username}, id : {current_user.ID}"
#   })

# @auth_views.route('/signup-page', methods=['GET'])
# def signup_page():
#   return render_template('signup.html')

# @auth_views.route('/signup', methods=['POST'])
# def signup_action():
#   data = request.form
#   staff = create_staff(data['username'], data['firstname'], data['lastname'], data['email'], data['password'], data['faculty'])
#   if not staff:
#     flash("Error creating user!")
#     return render_template('signup.html')
#   flash("User created!")
#   return render_template('login.html')

# # @auth_views.route('/login', methods=['POST'])
# # def login_action():
# #   data = request.form
# #   message="Bad username or password"
# #   user = login(data['username'], data['password'])
# #   if user:

# #     user_type = type(user)
# #     print("User type:", user_type)
# #     response = login_user(user)
# #     if (user.user_type == "staff"):
# #       return redirect(url_for("staff_views.get_StaffHome_page"))  # Redirect to student dashboard
# #   return render_template('login.html', message=message)

# # @auth_views.route('/login', methods=['POST'])
# # def login_page():
# #   data = request.form
# #   message="Bad username or password"
# #   user = login(data['username'], data['password'])
# #   if user:
# #     access_token = create_access_token(identity=user.ID)
# #     response = redirect(url_for('staff_views.get_StaffHome_page'))
# #     set_access_cookies(response, access_token)
# #   else:
# #     response = render_template('login.html', message=message)
# #   return response

# @auth_views.route('/login', methods=['POST'])
# def login_page():
#   data = request.form
#   message="Bad username or password"
#   user = login(data['username'], data['password'])
#   if user:
#     access_token = create_access_token(identity=user.ID)
#     response = redirect(url_for('staff_views.get_StaffHome_page'))
#     set_access_cookies(response, access_token)
#   else:
#     response = render_template('login.html', message=message)
#   return response

# @auth_views.route('/logout', methods=['GET'])
# def logout():
#   response = jsonify(message='Logged out')
#   unset_access_cookies(response)
#   return response

# # @auth_views.route('/logout', methods=['GET'])
# # def logout_action():
# #   logout_user()
# #   return redirect("/")


# '''
# API Routes
# '''


# @auth_views.route('/api/users', methods=['GET'])
# def get_users_action():
#   users = get_all_users_json()
#   return jsonify(users)


# @auth_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#   data = request.json
#   create_user(data['username'], data['password'])
#   return jsonify({'message': f"user {data['username']} created"})


# # @auth_views.route('/api/login', methods=['POST'])
# # def user_login_api():
# #   data = request.json
# #   token = jwt_authenticate(data['username'], data['password'])
# #   if not token:
# #     return jsonify(message='bad username or password given'), 401
# #   return jsonify(access_token=token)
# @auth_views.route('/api/login', methods=['POST'])
# def login_api_page():
#   data = request.json
#   message="Bad username or password"
#   user = login(data['username'], data['password'])
#   if user:
#     token = create_access_token(identity=user.ID)
#     response = jsonify(access_token=token)
#     set_access_cookies(response, token)
#   else:
#     response = render_template('login.html', message=message)
#   return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user_action():
#   user = jwt_current_user
#   return jsonify({
#       'message':
#       f"username: {jwt_current_user.username}, id : {jwt_current_user.ID}"
#   })

# @auth_views.route('/api/signup', methods=['POST'])
# def signup_api_action():
#   data = request.json
#   staff = create_staff(data['username'], data['firstname'], data['lastname'], data['email'], data['password'], data['faculty'])
#   if not staff:
#     return jsonify({"message": "Error creating user!"}), 400
#   flash("User created!")
#   return jsonify({"message": f"User {data['username']} created!"}), 200

from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import set_access_cookies,create_access_token,jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import Staff, Student, User
from App.controllers import (create_user, jwt_authenticate, login)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''


@auth_views.route('/users', methods=['GET'])
def get_user_page():
  users = get_all_users()
  return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
  return jsonify({
      'message':
      f"username: {current_user.username}, id : {current_user.ID}"
  })


@auth_views.route('/login', methods=['POST'])
def login_action():
  data = request.form
  message="Bad username or password"
  user = login(data['username'], data['password'])
  response = make_response(render_template('login.html', message=message))
  if user:
    user_type = type(user)
    print("User type:", user_type)
    login_user(user)
    if (user.user_type == "staff"):
      response = redirect(url_for("staff_views.get_StaffHome_page")) # Redirect to student dashboard
      set_access_cookies(response, create_access_token(identity=user.ID))
  return response


@auth_views.route('/logout', methods=['GET'])
def logout_action():
  logout_user()
  # data = request.form
  # user = login(data['username'], data['password'])
  #return 'logged out!'
  return redirect("/")


'''
API Routes
'''


@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
  users = get_all_users_json()
  return jsonify(users)


@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
  data = request.json
  create_user(data['username'], data['password'])
  return jsonify({'message': f"user {data['username']} created"})


@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
  return jsonify({
      'message':
      f"username: {jwt_current_user.username}, id : {jwt_current_user.ID}"
  })
