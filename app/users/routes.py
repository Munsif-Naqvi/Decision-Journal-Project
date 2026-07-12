from flask import Blueprint, jsonify, request
from app.users import services
from app.errors.exceptions import *
from app.users.schemas import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_bp.get("/ping")
def ping():
    return services.ping()


@users_bp.get("/me")
@jwt_required()
def me():
   user_id = int(get_jwt_identity())
   user = services.logged_in_user(user_id)
   return serialize_user(user), 200

@users_bp.post("/signup")
def signup():
    data = request.get_json()

    try:
        validated = validate_signup_data(data)

        user = services.create_user(
        name = validated['name'],
        email = validated['email'],
        password = validated['password']
    )
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "message": "User created successfully",
            }
        ), 201

    except ValidationError as e:
        return jsonify({
            "error": str (e)
        }), 400

    except EmailAlreadyExistsError as e:
        return jsonify({
            "error": "Email already exists"
        }), 409

@users_bp.post("/login")
def login():
    data = request.get_json()

    try:
        validated = validate_login_data(data)
        user = services.login_user(
            email = validated['email'],
            password = validated['password']
        )

        access_token = create_access_token(
            identity = str(user.id)
        )
        return jsonify(
            {
                "access_token": access_token
            }
        ), 200

    except ValidationError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except InvalidCredentialsError:
        return jsonify({
            "error": "Invalid email or password"
        }), 401
