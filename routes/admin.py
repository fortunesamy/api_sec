from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from marshmallow import ValidationError

from models import Admin, FoodCategory, db
from schema import AdminSchema



class RegisterAdmin(Resource):
    def post(self):
        try:
            data = AdminSchema().load(request.get_json())
            if Admin.query.filter_by(email=data['email']).first():
                return{"message": "Admin already exists"}, 400
            
            new_admin = Admin(
                         admin_name    =data['admin_name'],
                         email         =data['email'], 
                         password_hash =generate_password_hash(data['password_hash'], method='pbkdf2:sha1'),  
                         level         =data['level']
                         )

            db.session.add(new_admin)
            db.session.commit()

            return{"message": "Admin registered successfully", "user":AdminSchema().dump(new_admin)}, 201
        except ValidationError as err:
            return err.messages, 400 

class LoginAdmin(Resource):
    def post(self):
        data = request.get_json()
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin and check_password_hash(admin.password_hash,data['password_hash']):
            access_token = create_access_token(identity=admin.adminid)
            return{"access_token": access_token, "admin": {"userid": admin.adminid, "admin_name": admin.admin_name}}, 200
        return{"message": "invalid credentials"}, 401

class CreateFoodCategory(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()

        new_category = FoodCategory(category_name=data['category_name'], category_price=data['category_price'])

        db.session.add(new_category)
        db.session.commit()
        return{"message": "Category has been added successfully"}, 201
