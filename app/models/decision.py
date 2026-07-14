from datetime import datetime, UTC
from email.policy import default

from app.extensions.db import db

class Decision(db.Model):
    __tablename__ = 'decisions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

    user = db.relationship(
        "User",
        back_populates="decisions"
    )

    decision_statement = db.Column(db.Text, nullable=False) # what decision are you taking
    reasoning = db.Column(db.Text, nullable=False) # why are you taking this decision

    assumptions = db.Column(db.Text) # what are you expecting from this decision
    options_considered = db.Column(db.Text) # Any alternatives

    confidence_level = db.Column(db.Integer, nullable=False) # your confidence lvl while taking this decision
    expected_outcome = db.Column(db.Text, nullable=False) # what do you expect the result to be

    status = db.Column(db.String(20), nullable=False, default="OPEN") # is this decision ongoing or already reviewed
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "confidence_level >= 0 AND confidence_level <= 100",
            name="check_confidence_level"
        ),
    )