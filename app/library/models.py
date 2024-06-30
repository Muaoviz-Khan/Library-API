from app import db
from werkzeug.security import generate_password_hash,check_password_hash


user_books = db.Table(
    'user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(700), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=True) # admin for admin
    books = db.relationship("Book", secondary=user_books, backref='users', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not readable")
        
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_pass(self, password):
        return check_password_hash(self._password, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    genre = db.Column(db.String(50))
    count=db.Column(db.Integer,nullable=True)
    author_name = db.Column(db.String(30), db.ForeignKey('author.name'),nullable=True)

class Author(db.Model):
    name = db.Column(db.String(30),primary_key=True)
    bio = db.Column(db.Text)
    dob = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True)

