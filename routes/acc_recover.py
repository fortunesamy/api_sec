# API resources
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from flask_mail import Mail
from datetime import timedelta, datetime
import requests
# from app import db
from flask_restful import Resource


from models import Otp, User, db
from routes.auth import Login
from schema import OtpSchema, PasswordResetSchema, generate_otp, send_otp_email


# Resource to request OTP for password recovery
class RecoverPassword(Resource):
    def post(self):
        # Validate the request
        data = OtpSchema().load(request.get_json())

        email = data['email']

        # Check if the email exists (in real-life you'd query your DB)
        user = user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Email not found."}, 404

        # Check if OTP exists for this email and if it has expired
        existing_otp =  Otp.query.filter_by(email=email).first()
        if existing_otp:
            if datetime.now() - existing_otp.expiration < timedelta(minutes=10):
                return {"message": "Please wait. An OTP has been sent to your email."}

        # Generate a new OTP
        otp = generate_otp()
        # otp_record = Otp(email=email, otp=otp)

        # Save OTP in mock database (store in real database in production)
        otp_record = Otp(email=email, otp=otp)
        db.session.add(otp_record)
        db.session.commit()

        # Send the OTP to the user's email
        
        
        url = "https://api.postmarkapp.com/email"
        html = f"<html><body><strong>Hello</strong> dear food app user use the OTP:{otp} to confirm your account.</body></html>"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": "84c6cd00-4a43-4b9d-b837-8eb3da9fbc06",  # Replace with your Postmark server token
        }
       
        payload = {
        "From":"nnaemeka@zoetechglobalit.com",
        "To": email,
        "Subject": "food app password recovery",
        "TextBody": "Hello dear food app user.",
        "HtmlBody": html,
        "MessageStream": "outbound",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("Email sent successfully:", response.json())
            return {"message": "OTP sent successfully to your email."}
        else:
            print("Failed to send email:", response.status_code, response.json())

# Resource to verify OTP and reset password
class ResetPassword(Resource):
    def post(self):
        try:
            data = PasswordResetSchema().load(request.get_json())
        except ValidationError as err:
            return {"message": "Invalid data", "errors": err.messages}, 400

        email        = data['email']
        otp          = data["otp"]
        new_password = data['new_password']

        # Check if OTP exists for this email and verify it
        existing_otp    = Otp.query.filter_by(email=email).first()
        if not existing_otp or existing_otp.otp != otp:
            return {"message": "Invaid OTP."}, 401

        # Check if OTP has expired (10 minutes)
        timeDiff = datetime.now() - ( existing_otp.expiration + timedelta(hours=1) )
        if timeDiff  >= timedelta(minutes=10):
            return {"message": "OTP has expired.: {}".format(timeDiff)}, 400

        # Hash the new password before storing it
        new_password_hash = generate_password_hash(new_password, method='pbkdf2:sha1')

        # Update the user's password in the database
        user = User.query.filter_by(email=email).first()
        if user:
            user.password_hash = new_password_hash
            #  Delete OTP after use
            # del Otp[email]
            return {"message": "Password has been successfully updated."}


        # # Delete OTP after use
        try:
            db.session.delete(existing_otp)
            print("Delete Successfully")
        except Exception as e:
            print("Erro Occred deleting the OTP Record {}".format(e))
        db.session.commit()   

        return {"message": "Password has been successfully updated."}




# class VerifyEmail(Resource):
#     def post(self):
#         data = OtpSchema().load(request.get_json())
#         if Otp.query.filter_by(email=data['email']).first():
#             return{"message": "please wait"}
#         otp = Otp(Mail(data['otp']))
