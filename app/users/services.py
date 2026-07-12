import bcrypt
from flask import jsonify
from sqlalchemy.exc import IntegrityError

from app.extensions.db import db
from app.models import User
from app.errors.exceptions import *


def ping():
    return jsonify({
        "ping": "pong"
    })

def create_user(name, email, password):
    if User.query.filter_by(email=email).first():
        raise EmailAlreadyExistsError() # /*

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise

    return user

# we're returning two values here and (/* here). the user value and state which would be
# accepted in the routes.py as (user_data, success register_new_user(...)

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user is None:
        raise InvalidCredentialsError()

    password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
    )
    if not password_matches:
        raise InvalidCredentialsError()

    return user

def logged_in_user(id):
    user = db.session.get(User, int(id))
    if user is None:
        raise UserDoesNotExistError()

    return user