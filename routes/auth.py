# API resources
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
# from app import db
from flask_restful import Resource

from models import User, db
from schema import UserSchema


class Register (Resource):
    def post(self):
        try:
            data = UserSchema().load(request.get_json())
            if User.query.filter_by(username=data['username']).first():
                return{"message": "User already exists"}, 400
            
            new_user = User(
                         username       =data['username'],
                         email          =data['email'], 
                         password_hash  =generate_password_hash(data['password_hash'], method='pbkdf2:sha1'), 
                         phone_no       =data['phone_no'], 
                         address        =data['address'], 
                         role           =data['role']
                         )

            db.session.add(new_user)
            db.session.commit()

            return{"message": "User registered successfully", "user":UserSchema().dump(new_user)}, 201
        except ValidationError as err:
            return err.messages, 400

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash,data['password_hash']):
            access_token = create_access_token(identity=user.userid)
            return{"access_token": access_token, "user": {"userid": user.userid, "username": user.username}}, 200
        return{"message": "invalid credentials"}, 401