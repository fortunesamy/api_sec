from enum import Enum
from marshmallow import Schema, fields
from flask_mail import Mail, Message

import random

mail = Mail()


# Enum for Admin Levels
class AdminLevel(Enum):
    super_admin = "SuperAdmin"
    admin       = "Admin"

# Enum for Order and Payment Statuses
class Status(Enum):
    Pending    = "Pending"
    Successful = "Successful"
    Failed     = "Failed"
    Cancelled  = "Cancelled"

# for Validation with marshmallow Schema
class UserSchema(Schema):
    username = fields.String(required=True)
    email    = fields.String(required=True)
    password_hash = fields.String(required=True)
    phone_no = fields.String(required=True)
    address  = fields.String(required=True)
    role     = fields.String(required=False)

# user_schema = UserSchema()

class AdminSchema(Schema):
    admin_name    =fields.String(required=True)
    email         =fields.String(required=True)
    password_hash = fields.String(required=True)
    level         = fields.Enum((AdminLevel), required=True)

# admin_schema = AdminSchema()

# class OtpSchema(Schema):
#     email= fields.String(required=True)
#     otp=        fields.Integer(required=True)
#     expiration= fields.DateTime(required=True)

# Marshmallow Schemas
class OtpSchema(Schema):
    email = fields.Email(required=True)

class Otp:
    def __init__(self, email, otp, created_at):
        self.email = email
        self.otp = otp
        self.created_at = created_at

    def __repr__(self):
        return f'<Otp {self.otp} for {self.email}>'

class PasswordResetSchema(Schema):
    email        = fields.Email(required=True)
    otp          = fields.Integer(required=True)
    new_password = fields.String(required=True)

# OTP Generation function
def generate_otp():
    return random.randint(100000, 999999)

# Email sending function
def send_otp_email(email, otp):
    msg      = Message("Password Reset OTP", sender="fortunesamy01@gmail.com", recipients=[email])
    msg.body = f"Your OTP for password reset is {otp}. It will expire in 10 minutes."
    mail.send(msg)

class FoodCategorySchema(Schema):
    category_name = fields.String(required=True)
    category_price = fields.String(required=True)

# food_category_schema = FoodCategorySchema()


class OrderSchema(Schema):
    userid         = fields.Integer(required=True)
    order_name     = fields.String(required=True)
    order_price    = fields.String(required=True)
    order_quantity = fields.String(required = True)

# order_schema = OrderSchema()

class PaymentSchema(Schema):
    userid         = fields.Integer(required=True)
    orderid        = fields.Integer(required = True)
    amount         = fields.Integer(required = True)
    payment_method = fields.String(required=True)
    payment_status = fields.Enum((Status), required=True)
    transaction_id  = fields.String(required=True)
