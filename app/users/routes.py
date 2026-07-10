from flask import Blueprint, jsonify, request
from app.users import services
from app.errors.exceptions import EmailAlreadyExistsError, ValidationError
from app.users.schemas import validate_signup_data

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_bp.get("/ping")
def ping():
    return services.ping()

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