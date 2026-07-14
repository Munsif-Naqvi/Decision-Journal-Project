from app.extensions.db import db
from app.models import Decision
from sqlalchemy.exc import IntegrityError
from app.errors.exceptions import *

def create_decision(user_id, decision_data):

    decision = Decision(
        user_id=user_id,
        **decision_data
    )
    try:
        db.session.add(decision)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise

    return decision

def return_all_decisions(user_id):
    decisions = db.session.query(Decision).filter_by(user_id=user_id).all()
    if decisions is None:
        raise DecisionDoesNotExistError()
    return decisions

def return_one_decision(user_id, decision_id):
    one_decision = db.session.query(Decision).filter_by(user_id=user_id).filter_by(id=decision_id).first()
    if one_decision is None:
        raise DecisionDoesNotExistError()

    return one_decision

def update_one_decision(user_id, decision_id, decision_data):
    decision = db.session.query(Decision).filter_by(user_id=user_id).filter_by(id=decision_id).first()
    if decision is None:
        raise DecisionDoesNotExistError()

    if decision.status.lower() != "open":
        raise DecisionLockedError("Only decisions with an 'open' status can be updated.")

    for key, value in decision_data.items():
        setattr(decision, key, value)
        decision.user_id = user_id

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
    return decision
