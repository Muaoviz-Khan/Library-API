from flask import jsonify,request,Blueprint
from app import db
from app.library.serde import users_schema
from marshmallow import ValidationError
from app.library.models import User

register=Blueprint("register",__name__)

@register.route('/register', methods=['POST'])
def post():
    data = request.get_json()

    try:
        va = users_schema().load(data)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors':e}), 422

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    if len(data["name"]) < 2:
        return jsonify({'message': 'First name must be greater than 1 character.'}), 400
    
    if len(data["password"]) < 7:
        return jsonify({'message': 'Password must be at least 7 characters.'}), 400
    
    user = User(
        name=data['name'],
        username=data['username'],
        password=data['password'],
        email=data['email'],
        status=data.get('status'),

    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})