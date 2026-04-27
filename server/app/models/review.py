from datetime import datetime
from . import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    media_id = db.Column(db.String(50), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)   # movie | tv | game | book
    title = db.Column(db.String(255), nullable=False)       # media title (for display)
    image_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Integer, nullable=False)          # 1–5 user star rating
    body = db.Column(db.Text, nullable=True)                # optional written review
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'media_id', 'media_type', name='uq_user_review'),
    )

    def to_dict(self, include_username=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'media_id': self.media_id,
            'media_type': self.media_type,
            'title': self.title,
            'image_url': self.image_url,
            'rating': self.rating,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
        }
        if include_username:
            data['username'] = self.user.username if self.user else 'Unknown'
        return data
