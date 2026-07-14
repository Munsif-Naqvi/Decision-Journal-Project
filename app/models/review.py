from datetime import datetime, UTC

from app.extensions.db import db

class Review(db.Model):
    __tablename__ = 'reviews'
    decision = db.relationship(
        "Decision",
        back_populates="review"
    )

    id = db.Column(db.Integer, primary_key=True)

    actual_outcome = db.Column(db.Text, nullable=False)  # what became of your decision
    reflection = db.Column(db.Text, nullable=False)  # looking back to the decision

    lessons_learned = db.Column(db.Text)  # what did you learn from taking that decision
    would_make_same_decision = db.Column(db.Boolean, nullable=False)  # Any alternatives

    reviewed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )
    decision_id = db.Column(
        db.Integer,
        db.ForeignKey('decisions.id'),
        nullable=False,
        unique=True
    )