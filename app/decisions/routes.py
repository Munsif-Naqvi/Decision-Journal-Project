from flask import Blueprint, jsonify, request
from app.decisions import services
from app.decisions.schemas import *
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.decisions.services import *

decisions_bp = Blueprint("decisions", __name__, url_prefix="/api/v1/decisions")

@decisions_bp.get("/ping")
def ping():
    return {"ping": "pong"}

@decisions_bp.post("/decision")
@jwt_required()
def create_decision():

    try:
        user_id = int(get_jwt_identity())
    except InvalidTokenError:
        return jsonify({
            "error": "Invalid User Identity Token"
        }), 422
    try:
        data = request.get_json()
        validated_data = validate_decision_data(data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

   # Assuming your service returns the created decision or its ID
    new_decision = services.create_decision(user_id, validated_data)

    return jsonify({
                "message": "Decision created",
                "decision_id": getattr(new_decision, 'id', None),  # Good practice to return the new resource ID
                "user_id": user_id
            }), 201


@decisions_bp.get("/decisions")
@jwt_required()
def get_all_decisions():

    try:
        user_id = int(get_jwt_identity())
    except InvalidTokenError:
        return jsonify({
            "error": "Invalid User Identity Token"
        }), 401

    try:
        decisions = return_all_decisions(user_id)
        return jsonify(serialize_decisions(decisions)), 200

    except DecisionDoesNotExistError:
        return jsonify({
            "error": "Decision does not exist"
        }), 404

@decisions_bp.get("/decision/<int:decision_id>")
@jwt_required()
def get_one_decision(decision_id):
    try:
        user_id = int(get_jwt_identity())
    except (ValueError, TypeError):
        return jsonify({"error": "Malformed user identity in token"}), 422

    try:
        one_decision = return_one_decision(user_id,decision_id)
        return jsonify(serialize_decision(one_decision)), 200

    except DecisionDoesNotExistError:
        return jsonify({
            "error": "Decision does not exist"
        }), 404

@decisions_bp.put("/decision/<int:decision_id>")
@jwt_required()
def update_decision(decision_id):
    try:
        user_id = int(get_jwt_identity())
    except (ValueError, TypeError):
        return jsonify({"error": "Malformed user identity in token"}), 422
    data = request.get_json()

    try:
        validated_data = validate_decision_data(data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    try:
        updated_decision = update_one_decision(
            user_id=user_id,
            decision_id=decision_id,
            decision_data=validated_data
        )

        return jsonify({
            "message": "Decision updated successfully",
            "decision": serialize_decision(updated_decision)  # Returning the updated resource is standard REST practice
        }), 200

    except DecisionDoesNotExistError as e:
        return jsonify({
            "error": str(e)
        }), 400
    except DecisionAlreadyReviewedError:
        return jsonify({
            "error": "Cannot update an already reviewed decision"
        }), 400

@decisions_bp.get("/")
@jwt_required()
def get_decisions_by_status():
    try:
        user_id = int(get_jwt_identity())
    except (ValueError, TypeError):
        return jsonify({"error": "Malformed user identity in token"}), 422

    status_filter = request.args.get("status")

    if status_filter:
        status_filter = status_filter.strip().upper()

        try:
            decisions = return_decisions_with_status(user_id, status_filter)
            return jsonify(serialize_decisions(decisions)), 200

        except DecisionDoesNotExistError as e:
            return jsonify({

                "error": str(e) if str(e) else f"Invalid status. '{status_filter}'"

            }), 400
