import json

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from server.app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

flask_bcrypt = Bcrypt()
flask_bcrypt.init_app(app)

manager = Manager(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/create')
def create_user():
    # try:
    user = User(age=22, name="vk59", gender='male')
    db.session.add(user)
    db.session.commit()
    return app.response_class(
        response=json.dumps(user, cls=UserEncoder),
        status=200,
        mimetype='application/json'
    )
    # except Exception as e:
    #     return app.response_class(response=jsonify({"error": str(e.__cause__)}),
    #                               status=500,
    #                               mimetype='application/json')


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, default="")
    age = db.Column(db.Integer, nullable=False, default=-1)
    gender = db.Column(db.String(10), nullable=False, default='-')

    def __repr__(self):
        return "<user '{}'>".format(self.id)


class UserEncoder(json.JSONEncoder):

    def default(self, u):

        if isinstance(u, User):
            dict = {
                "id": u.id,
                "name": u.name,
                "age": u.age,
                "gender": u.gender
            }
            return dict
        else:
            type_name = u.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))

