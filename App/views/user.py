from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    
    # Check if required fields are in the request
    if not data or 'username' not in data or 'firstname' not in data or 'lastname' not in data or 'password' not in data or 'email' not in data or 'faculty' not in data:
        return jsonify({'message': 'Missing required fields: username, firstname, lastname, password, email, or faculty'}), 400
    
    # Call the function to create the user if data is valid
    create_user(data['username'], data['firstname'], data['lastname'], data['password'], data['email'], data['faculty'])
    
    return jsonify({'message': f"user {data['username']} created"}), 201


@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['firstname'], data['lastname'], data['password'], data['email'], data['faculty'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')