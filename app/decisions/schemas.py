from app.errors.exceptions import *


def validate_decision_data(decision_data: dict) -> dict:

    if not isinstance(decision_data, dict):
        raise ValidationError("Request body must be valid JSON")

    # For title
    title = decision_data.get("title")
    if title is None:
        raise ValidationError("Title is required")

    if not isinstance(title, str):
        raise ValidationError("Title must be a string")

    title = title.strip()
    if not title:
        raise ValidationError("Title must not be empty")

    if len(title) > 150:
        raise ValidationError("Title cannot exceed 150 characters")

    # For decision_statement
    decision_statement = decision_data.get("decision_statement")
    if decision_statement is None:
        raise ValidationError("Decision statement is required")

    if not isinstance(decision_statement, str):
        raise ValidationError("Decision statement must be a string")

    decision_statement = decision_statement.strip()
    if not decision_statement:
        raise ValidationError("Decision statement must not be empty")

    # For reasoning
    reasoning = decision_data.get("reasoning")
    if reasoning is None:
        raise ValidationError("Reasoning is required")

    if not isinstance(reasoning, str):
        raise ValidationError("Reasoning must be a string")

    reasoning = reasoning.strip()
    if not reasoning:
        raise ValidationError("Reasoning must not be empty")

    # For assumptions (Nullable in DB)
    assumptions = decision_data.get("assumptions")
    if assumptions is not None:
        if not isinstance(assumptions, str):
            raise ValidationError("Assumptions must be a string")
        assumptions = assumptions.strip()
    else:
        assumptions = ""

    # For options_considered (Nullable in DB)
    options_considered = decision_data.get("options_considered")
    if options_considered is not None:
        if not isinstance(options_considered, str):
            raise ValidationError("Options considered must be a string")
        options_considered = options_considered.strip()
    else:
        options_considered = ""

    # For confidence_level
    confidence_level = decision_data.get("confidence_level")
    if confidence_level is None:
        raise ValidationError("Confidence level is required")

    # If it comes as a string representation of an int, safely parse it
    if isinstance(confidence_level, str) and confidence_level.isdigit():
        confidence_level = int(confidence_level)

    if not isinstance(confidence_level, int) or isinstance(confidence_level, bool):
        raise ValidationError("Confidence level must be an integer")

    if confidence_level < 0 or confidence_level > 100:
        raise ValidationError("Confidence level must be between 0 and 100")

    # For expected_outcome
    expected_outcome = decision_data.get("expected_outcome")
    if expected_outcome is None:
        raise ValidationError("Expected outcome is required")

    if not isinstance(expected_outcome, str):
        raise ValidationError("Expected outcome must be a string")

    expected_outcome = expected_outcome.strip()
    if not expected_outcome:
        raise ValidationError("Expected outcome must not be empty")

    # For status (providing a default)
    status = decision_data.get("status")
    if status is not None:
        if not isinstance(status, str):
            raise ValidationError("Status must be a string")
        status = status.strip()
        if not status:
            raise ValidationError("Status must not be empty")
    else:
        status = "OPEN"

    return {
        "title": title,
        "decision_statement": decision_statement,
        "reasoning": reasoning,
        "assumptions": assumptions,
        "options_considered": options_considered,
        "confidence_level": confidence_level,
        "expected_outcome": expected_outcome,
        "status": status
    }

def serialize_decision(decision):
    return {
        "id": decision.id,
        "title": decision.title,
        "decision_statement": decision.decision_statement,
        "reasoning": decision.reasoning,
        "assumptions": decision.assumptions,
        "options_considered": decision.options_considered,
        "confidence_level": decision.confidence_level,
        "expected_outcome": decision.expected_outcome,
        "status": decision.status,
        "created_at": decision.created_at.isoformat() if decision.created_at else None,
        "updated_at": decision.updated_at.isoformat() if decision.updated_at else None
    }

def serialize_decisions(decisions_list) -> list:
    # Uses a list comprehension to loop through every decision in the list
    return [serialize_decision(decision) for decision in decisions_list]