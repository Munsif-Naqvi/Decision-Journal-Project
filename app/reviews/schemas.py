from app.errors.exceptions import *

def validate_review_data(review_data: dict) -> dict:

    if not isinstance(review_data, dict):
        raise ValidationError("Request body must be valid JSON")

    # For actual_outcome
    actual_outcome = review_data.get("actual_outcome")
    if actual_outcome is None:
        raise ValidationError("Actual outcome is required")

    if not isinstance(actual_outcome, str):
        raise ValidationError("Actual outcome must be a string")

    actual_outcome = actual_outcome.strip()
    if not actual_outcome:
        raise ValidationError("Actual outcome must not be empty")

    # For reflection
    reflection = review_data.get("reflection")
    if reflection is None:
        raise ValidationError("Reflection is required")

    if not isinstance(reflection, str):
        raise ValidationError("Reflection must be a string")

    reflection = reflection.strip()
    if not reflection:
        raise ValidationError("Reflection must not be empty")

    # For lessons_learned
    lessons_learned = review_data.get("lessons_learned")
    if lessons_learned is not None:
        if not isinstance(lessons_learned, str):
            raise ValidationError("Lessons learned must be a string")
        lessons_learned = lessons_learned.strip()
    else:
        lessons_learned = ""

    # For would_make_same_decision
    would_make_same_decision = review_data.get("would_make_same_decision")
    if would_make_same_decision is None:
        raise ValidationError("Response to 'would make same decision' is required")

    if not isinstance(would_make_same_decision, bool):
        raise ValidationError("Response to 'would make same decision' must be a boolean (true/false)")

    return {
        "actual_outcome": actual_outcome,
        "reflection": reflection,
        "lessons_learned": lessons_learned,
        "would_make_same_decision": would_make_same_decision,
    }

def serialize_review(review):
    return {
        "actual_outcome": review.actual_outcome,
        "reflection": review.reflection,
        "lessons_learned": review.lessons_learned,
        "would_make_same_decision": review.would_make_same_decision,
    }