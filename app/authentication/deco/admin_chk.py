from flask import session,jsonify
from app.library.models import User
from functools import wraps


def admin_only(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        member=User.query.filter_by(id=session.get('id')).first()
        if member.status == "admin":
            return f(*args,**kwargs)
        else:
            return jsonify({'message':'only admins access'}),403   
    return decorated    