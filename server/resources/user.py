# resources/user.py

from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
from models import User, db

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', required=True, help="Name is required")
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()
        data['password'] = generate_password_hash(data['password']).decode('utf-8')

        email = User.query.filter_by(email=data['email']).first()

        if email:
            return {"message": "Email address already taken", "status": "fail"}, 422

        user = User(**data)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully", "status": "success", "user": user.to_dict()}

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()

        if user and user.check_password(data['password']):
            user_dict = user.to_dict()
            return {"message": "Login successful", "status": "success", "user": user_dict}
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 403
