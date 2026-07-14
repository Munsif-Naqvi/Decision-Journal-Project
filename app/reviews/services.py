from app.extensions.db import db
from app.models import Review, Decision
from sqlalchemy.exc import IntegrityError
from app.errors.exceptions import *

def review_decision(user_id, decision_id, review_data):

    get_decision = db.session.query(Decision).filter_by(user_id=user_id).filter_by(id=decision_id).first()
    if get_decision is None:
        raise DecisionDoesNotExistError()

    if get_decision.status.lower() != "open":
        raise DecisionAlreadyReviewedError()

    try:
        # 3. Create and populate the new Review record
        new_review = Review(
            decision_id=decision_id,
            **review_data  # Cleanly unpack all validated review fields (outcome, reflection, etc.)
        )
        db.session.add(new_review)

        get_decision.status = "REVIEWED"

    # 5. Commit both operations atomically in a single transaction
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
# Raise a clean exception or log the error
        raise ValueError("Could not save review due to a database constraint conflict.") from e

    return new_review