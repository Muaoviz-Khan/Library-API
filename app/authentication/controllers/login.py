from flask import jsonify,request,Blueprint,current_app,session
import jwt
from app.library.serde import users_schema
from marshmallow import ValidationError
from app.library.models import User
from datetime import datetime, timedelta,timezone

login=Blueprint("login",__name__)


@login.route('/login', methods=['POST'])
def post():
    credentials = request.get_json()
    user = User.query.filter_by(username=credentials["username"]).first()

    try:
        va = users_schema().load(credentials)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors':e}), 422
    
    if not user or not user.verify_pass(credentials["password"]):
        return jsonify({'message': 'Invalid username or password'}), 401

    session['id'] = user.id
    print("Session after login:", session)  # Debug print
    print("User's ID:", user.id)

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=100)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    response = jsonify({'message':'login successfull','token': token})
    response.set_cookie("token", token, httponly=True) 
    return response