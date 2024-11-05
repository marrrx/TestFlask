# app.py
from flask import Flask
from flask_restful import Api
from api.controllers import createUser, deleteUser, readUsers, readUser, tryGet, updateUser
from api.extension import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:8889/flask"
api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()

# API ROUTES
api.add_resource(createUser, "/api/users/register")
api.add_resource(readUsers, "/api/users")
api.add_resource(readUser, "/api/users/<int:id>")
api.add_resource(updateUser, "/api/users/<int:id>")
api.add_resource(deleteUser, "/api/users/<int:id>")
api.add_resource(tryGet, "/api/users/try")

if __name__ == "__main__":
    app.run(debug=True)

