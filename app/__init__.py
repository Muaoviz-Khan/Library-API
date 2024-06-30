from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()
def create_database(app, db):
    
        with app.app_context():
            db.create_all()
            print('database created')


def create_app():
    
    app=Flask(__name__)
    app.config['SECRET_KEY']="!DW#(32RR)>&WHsai23"
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:muaoviz@localhost:5432/library"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    

    from .authentication.controllers.login import login
    app.register_blueprint(login,url_prefix='/api/auth/')
    from .authentication.controllers.logout import logout
    app.register_blueprint(logout,url_prefix='/api/auth/')
    from .authentication.controllers.register import register
    app.register_blueprint(register,url_prefix='/api/auth/')

    from .library.library import user_op
    app.register_blueprint(user_op,url_prefix='/library/')
    
    create_database(app, db)

    return app  


    