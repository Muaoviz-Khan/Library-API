from marshmallow import Schema, fields

class users_schema(Schema):
    id = fields.Int()
    name=fields.Str()
    username = fields.Str()
    password = fields.Str()
    email = fields.Email()
    status = fields.Str(allow_none=True, validate=lambda s: s in [None, "admin"])


class books_schema(Schema):
    id = fields.Int()
    title = fields.Str()
    publication_date = fields.Date()
    genre = fields.Str()
    count=fields.Int()
    author_name = fields.Str ()
   

class author_schema(Schema):
    name = fields.Str()
    bio = fields.Str()
    dob = fields.Date()