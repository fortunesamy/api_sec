from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models import Order, db
from schema import OrderSchema


class MakeOrder(Resource):
    @jwt_required()
    def post(self):
        # data = request.get_json()
        data = OrderSchema().load(request.get_json())
        new_order = Order(userid=data['userid'], order_name=data['order_name'], order_price=data['order_price'], order_quantity=data['order_quantity'])

        db.session.add(new_order)
        db.session.commit()
        return{"message": "Order has been placed successfully"}, 201