from flask import Blueprint

user_api = Blueprint('user_api', __name__)

@user_api.route('/user/info')
def userInfo():
    return "This is user info"