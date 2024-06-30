from flask import Blueprint,jsonify,request,session
from app.authentication.deco.token_req import token_required
from app.authentication.deco.admin_chk import admin_only
from app.library.models import Book,User,Author
from app import db
from app.library.serde import books_schema,author_schema,users_schema
from marshmallow import ValidationError


user_op=Blueprint("user_op",__name__)


#check all the books available
@user_op.route("/view_books",methods=['GET'])
@token_required
def get_books():
    books = Book.query.all()
    output = books_schema(many=True).dump(books)
    return jsonify(output)


#add books
#send book data in json list of dictionary
@user_op.route("/add_books",methods=['POST'])
@token_required
@admin_only
def add_books():
    if not (data := request.get_json()):
        return jsonify({'message': 'no data '}), 204
    print(data)
    try:
        book_list = books_schema(many=True).load(data)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'errors': e.messages}), 422
    
    

    books_to_add = []
    for book_data in book_list:
        authorname = book_data.get('author_name')
        author = Author.query.filter_by(name=authorname).first()

    # If author doesn't exist, insert author first
        if not author:
            author = Author(name=authorname)
            db.session.add(author)
            db.session.commit()
        existing_book = Book.query.filter_by(title=book_data['title']).first()

        if existing_book and book_data['publication_date'] == existing_book.publication_date:
            existing_book.count = existing_book.count + book_data.get('count', 1)
            db.session.add(existing_book)  # Update the existing book      doubt
        else:
            new_book = Book(**book_data)
            books_to_add.append(new_book)
    
    if books_to_add:
        db.session.bulk_save_objects(books_to_add)
    
    db.session.commit()
    return jsonify({'message': 'Books added successfully'}), 201


#update book details
@user_op.route("/update_book/<int:book_id>",methods=['PUT'])
@token_required
@admin_only
def update_book(book_id):
    if not (data := request.get_json()):
        return jsonify({'message': 'no data '}), 204
    print(data)
    try:
        book_data = books_schema().load(data,partial=True)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'errors': e.messages}), 422
    book=Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    for key, value in book_data.items():
        setattr(book, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Book updated successfully'}), 200


#search details about a single book 
@user_op.route("/Search_book/<string:book_name>",methods=['GET'])
@token_required
def search_book(book_name):
    book = Book.query.filter_by(title=book_name).first()
    if not book:
        return jsonify({'message':"Book not available"}),404
    return jsonify(books_schema().dump(book)),200


#issue book
@user_op.route("/issue_book/<string:book_name>",methods=['GET'])
@token_required
def issue_book(book_name):
    user_id=session.get('id')
    user=User.query.get(user_id)
    

    book = Book.query.filter_by(title=book_name).first()
    if not book:
        return jsonify({'message':"Book not available"}),404
    
    if book.count<=0:
        return jsonify({'message':'Book currently not available'})
    
    if book in user.books:
        return jsonify({'message':'you have already issued the book'})

    book.count -= 1

    user.books.append(book)

    db.session.commit()
    return jsonify({'message':f'Book:{book_name} Borrowed'}),200


#return book
@user_op.route("/return_book/<string:book_name>",methods=['GET'])
@token_required
def return_book(book_name):
    user_id=session.get('id')
    user=User.query.get(user_id)

    book = Book.query.filter_by(title=book_name)
    if not book:
        return jsonify({'message':"Book does not belong to this library"}),404
    
    
    book.count += 1
    user.books.remove(book)
    db.session.commit()
        
    return jsonify({'message':f'Book:{book_name} returned successfully'}),200


#delete book
@user_op.route("/delete_book/<string:book_name>",methods=['DELETE'])
@token_required
@admin_only
def delete_book(book_name):
    book=Book.query.filter_by(title=book_name).first()
    if not book:
        return jsonify({'message':f'Book:{book_name}does not exist'}),404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message':f'book:{book_name} deleted successfully'}),200




#know who borrowed the book
@user_op.route("/issued_by/<string:book_name>",methods=['GET'])
@token_required
@admin_only
def issued_by(book_name):
    book=Book.query.filter_by(title=book_name).first()
    if not book :
        return jsonify({'message':'Book does not exist'})
    allusers=book.users
    output=users_schema(many=True).dump(allusers)
    return jsonify({f'{book_name} is borrowed by':output})


#books borrowed by specific user
@user_op.route("/issued_book/<int:user_id>",methods=['GET'])
@token_required
@admin_only
def issued_book(user_id):
    user=User.query.get(user_id)
    if not user:
        return jsonify({'message':'Book does not exist'})
    allbooks=user.books
    output=books_schema(many=True).dump(allbooks)
    return jsonify({f'books borrowed by {user.name}':output})


#check all the authors
@user_op.route("/view_authors",methods=['GET'])
@token_required
def get_authors():
    authors = Author.query.all()
    output = author_schema(many=True).dump(authors)
    return jsonify(output)



#uplaod json list of dictionaries ,can enter multiple author details at once
@user_op.route("/add_authors",methods=['POST'])
@token_required
@admin_only
def add_authors():
    if not (data := request.get_json()):
        return jsonify({'message': 'no data '}), 204
    print(data)
    try:
        auth_list = author_schema(many=True).load(data)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'errors': e.messages}), 422
    
    auth_to_add = []
    for auth_data in auth_list:
        existing_auth =Author.query.get(auth_data['name'])

        if existing_auth and existing_auth.bio:
            if len(auth_list)==1:
                return jsonify({'message':'author already Exists'})
            else:
                continue

        if existing_auth and not existing_auth.bio:
            existing_auth.dob=auth_data.get('dob')
            existing_auth.bio=auth_data.get('bio')
            
        else:
            new_auth = Author(**auth_data)
            auth_to_add.append(new_auth)
    
    if auth_to_add:
        db.session.bulk_save_objects(auth_to_add)
    
    db.session.commit()
    return jsonify({'message': 'Authors details added successfully '}), 201  


#delete author
@user_op.route("/delete_auth/<string:auth>",methods=['DELETE'])
@token_required
@admin_only
def delete_auth(auth):
    autho=Author.query.get(auth)
    if not autho:
        return jsonify({'message':f'author:{autho}does not exist'}),404
    db.session.delete(autho)
    db.session.commit()
    return jsonify({'message':f'author details of :{autho}deleted successfully'}),200


#all the books from a specific author
@user_op.route("/authors_book/<string:auth_name>",methods=['GET'])
@token_required
def authors_book(auth_name):
    authorr=Author.query.get(auth_name)
    if not authorr:
        return jsonify({'message':'no such author or incorrect author name'})
    if not authorr.books:
        return jsonify({'message':'no books registered with this author name'})
    allbooks=authorr.books
    out=books_schema(many=True).dump(allbooks)
    return jsonify({f'all books from author {auth_name}': out})


#author of a specific book
@user_op.route("/books_author/<string:book_name>",methods=['GET'])
@token_required
def books_author(book_name):
    book_=Book.query.filter_by(title=book_name).first()
    if not book_:
        return jsonify({'message':f'Book:{book_name} does not exist'})

    author_=book_.author
    if not author_:
        return jsonify({'message':f'Book:{book_name} author does not exist'})
    
    out=author_schema().dump(author_)
    return jsonify({f"Author of the book '{book_name}'":out})
    
