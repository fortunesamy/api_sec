from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from enum import Enum

from models import Payment, db
from schema import Status

class MakePayment(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_payment = Payment(userid=data['userid'], orderid=data['orderid'],amount=data['amount'], payment_method=data['payment_method'], payment_status=data['payment_status'], transaction_id=data['transaction_id'])

        
        db.session.add(new_payment)
        db.session.commit()
        return{"message": "payment successful"}, 201
