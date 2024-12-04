from flask_login import login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, JWTManager
from flask import jsonify
from App.models import User

def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # print("User:", user.firstname)
        return user
    return None

def login_user(userObj):
  user = userObj
  if user and user.check_password(user.password):
    token = create_access_token(identity=user.username)
    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response
  return jsonify(message="Invalid username or password"), 401

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.ID
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt