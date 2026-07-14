from flask import Blueprint, jsonify, request
from app.reviews.services import *
from app.reviews.schemas import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.reviews.services import *

reviews_bp = Blueprint("reviews", __name__, url_prefix="/api/v1/reviews")

@reviews_bp.post('/decisions/<int:decision_id>/review')
@jwt_required()
def create_review(decision_id):
    try:
        user_id = int(get_jwt_identity())
    except (ValueError, TypeError):
        return jsonify({"error": "Malformed user identity in token"}), 422

    review_data = request.get_json()
    try:
        validated_data=validate_review_data(review_data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    try:
        review = review_decision(
        user_id,
        decision_id,
        validated_data
        )
        return jsonify({
        "message": "Review added successfully",
        "review": serialize_review(review)
    }), 200

    except DecisionDoesNotExistError as e:
        return jsonify({
            "error": str(e)
        }), 404

    except DecisionAlreadyReviewedError:
        return jsonify({
            "error": "Cannot update an already reviewed decision"
        }), 400


