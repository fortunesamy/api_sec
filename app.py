from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
import os 

# from models         import FoodCategory, db
from routes.admin   import CreateFoodCategory, LoginAdmin, RegisterAdmin
from routes.auth    import Login, Register
from routes.order   import MakeOrder
from routes.payment import MakePayment
from routes.acc_recover import RecoverPassword, ResetPassword
from models import db
from schema import mail

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"]              = os.getenv('SECRET_KEY')
app.config["JWT_SECRET_KEY"]          = os.getenv('JWT_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER']             = os.getenv('MAIL_SERVER')  # Example: Gmail SMTP server
# app.config['MAIL_PORT']               = 25
# app.config['MAIL_USE_TLS']            = False
# app.config['MAIL_USE_SSL']            = False
# app.config['MAIL_USERNAME']           = None
# app.config['MAIL_PASSWORD']           = None


api = Api(app)
CORS(app)
db.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)
# db  = SQLAlchemy(app)
# db  = db(app)



   # users endpoints
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(MakeOrder, '/order')
api.add_resource(MakePayment, '/payment')
api.add_resource(RecoverPassword,'/recover')
api.add_resource(ResetPassword, '/reset')

# admin endpoints
api.add_resource(RegisterAdmin,'/create-admin')
api.add_resource(LoginAdmin,'/admin-login')
api.add_resource(CreateFoodCategory, '/food')


if __name__ == '__main__':
    app.run(debug=True)



