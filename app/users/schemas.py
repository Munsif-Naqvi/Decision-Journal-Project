import re
from app.errors.exceptions import ValidationError

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def validate_signup_data(data: dict) -> dict:

    if not isinstance(data, dict):
        raise ValidationError("Request body must be valid JSON")

    # For Name

    name = data.get("name")

    if name is None:
        raise ValidationError("Name is required")

    if not isinstance(name, str):
        raise ValidationError("Name must be a string")

    name = name.strip()
    if not name:
        raise ValidationError("Name must not be empty")

    if len(name) > 100:
        raise ValidationError("Name cannot exceed 100 characters")

    # For Email

    email = data.get("email")

    if email is None:
        raise ValidationError("Email is required")

    if not isinstance(email, str):
        raise ValidationError("Email must be a string")

    email = email.strip().lower()
    if len(email) > 255:
        raise ValidationError("Email cannot exceed 255 characters")

    if not EMAIL_REGEX.fullmatch(email):
        raise ValidationError("Invalid email address")

    # For password

    password = data.get("password")
    if password is None:
        raise ValidationError("Password is required")

    if not isinstance(password, str):
        raise ValidationError("Password must be a string")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")

    return {
        "name": name,
        "email": email,
        "password": password,
    }