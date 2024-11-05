import json
from flask import Flask, Response, abort
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from .extension import db
from .models import User
import re

###### ARGUMENTS #######
create_user_args = reqparse.RequestParser()
create_user_args.add_argument("name", type=str, required=True, help="Name is required")
create_user_args.add_argument(
    "email", type=str, required=True, help="Email is required"
)
create_user_args.add_argument(
    "password", type=str, required=True, help="Password is required"
)

update_user_args = reqparse.RequestParser()
update_user_args.add_argument("name", type=str, help="Name is optional")
update_user_args.add_argument("email", type=str, help="Email is optional")
update_user_args.add_argument("password", type=str, help="Password is optional")
###########

###### FORMATTING RESPONSE ########
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
}
######################


##### USER CONTROLLER WITH METHODS ######
class tryGet(Resource):
    def get(self):
        print("Reached readUsers GET method")
        return {"message": "Success"}, 200 
    
class createUser(Resource):
    @marshal_with(userFields)
    def post(self):
        args = create_user_args.parse_args()

        errors = []

        # Validate email 
        if not args["name"] or args["name"].isspace():
            errors.append("Name is required")

        # Validate email
        if not args["email"] or args["email"].isspace():
            errors.append("Email is required")
        else:
            email = args["email"].strip()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Invalid email format")

        # Validate password
        if not args["password"] or args["password"].isspace():
            errors.append("Password is required")
        else:
            password = args["password"].strip()
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            if not any(char.isdigit() for char in password):
                errors.append("Password must contain at least one digit")
            if not any(char.isupper() for char in password):
                errors.append("Password must contain at least one uppercase letter")

        # If errors, send the response
        if errors:
            response = Response(
                json.dumps({"errors": errors}),
                status=400,
                mimetype="application/json",
            )
            return abort(response)

        name = args["name"]
        email = args["email"]
        password = args["password"]

        hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")

        # Verify if the user exists
        if User.query.filter_by(email=email).first():
            return {"message": "User with that email already exists"}, 400

        # Create new user
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return user, 201



#### READ USERS ######
class readUsers(Resource):
    @marshal_with(userFields)
    def get(self):
        users = User.query.all()
        return users, 201


#### READ USER ######
class readUser(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = db.session.get(User, id)
        return user, 201


#### UPDATE USER ######
class updateUser(Resource):
    @marshal_with(userFields)
    def put(self, id):
        user = db.session.get(User, id)
        if not user:
            return {"message": "User not found"}, 404

        args = update_user_args.parse_args()
        if args["name"]:
            user.name = args["name"]
        if args["email"]:
            user.email = args["email"]
        if args["password"]:
            user.password = (
                Bcrypt().generate_password_hash(args["password"]).decode("utf-8")
            )

        db.session.commit()
        return user, 200


#### DELETE USER ######
class deleteUser(Resource):
    def delete(self, id):
        user = db.session.get(User, id)
        if not user:
            return {"message": "User not found"}, 404
        if user:
            db.session.delete(user)
            db.session.commit()
        return {"message": "User deleted successfully"}, 200


######################
