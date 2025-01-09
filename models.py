from datetime import datetime
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from schema import AdminLevel, Status
from flask_mail import Mail
# from app import app

mail = Mail()
db  = SQLAlchemy()

# Database Model
class User(db.Model):
    userid          = db.Column(db.Integer, primary_key = True)
    username        = db.Column(db.String(100), unique = True, nullable =  False)
    email           = db.Column(db.String(50), unique = True, nullable = False)
    password_hash   = db.Column(db.String(100), nullable = False)
    phone_no        = db.Column(db.String(12), nullable = True)
    address         = db.Column(db.String(200), nullable = False)
    role            = db.Column(db.String(30), default = "User", nullable = False)
    created_at      = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class Admin(db.Model):
    adminid       = db.Column(db.Integer, primary_key = True)
    admin_name    = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    level         = db.Column(db.Enum(AdminLevel), nullable=False, default=AdminLevel.admin)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class Otp(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(100), nullable=False)
    otp        = db.Column(db.Integer, nullable=False)
    expiration = db.Column(db.DateTime,default=datetime.utcnow() + timedelta(minutes=10), nullable=False)
    

class FoodCategory(db.Model):
    categoryid          = db.Column(db.Integer, primary_key = True)
    category_name       = db.Column(db.String(100), nullable =  False)
    category_price      = db.Column(db.String(40), nullable = False)
    created_at          = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

class Order(db.Model):
    orderid        = db.Column(db.Integer, primary_key =  True)
    userid         = db.Column(db.Integer, db.ForeignKey("user.userid"), unique = False, nullable=False)
    order_name     = db.Column(db.String(70), nullable = False)
    order_price    = db.Column(db.String(40), nullable = False)
    order_quantity = db.Column(db.String(40), nullable = False)
    created_at     = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

class Payment(db.Model):
    paymentid      = db.Column(db.Integer, primary_key =  True)
    userid         = db.Column(db.Integer, db.ForeignKey("user.userid"), unique = False, nullable = False)
    order_id       = db.Column(db.Integer, db.ForeignKey("order.orderid"), nullable = False)
    amount         = db.Column(db.String(40), nullable = False)
    payment_method = db.Column(db.String(30), nullable = False)
    payment_status = db.Column(db.Enum(Status), nullable=False, default=Status.Pending)
    transaction_id = db.Column(db.String(100), nullable  = False)
    created_at     = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

