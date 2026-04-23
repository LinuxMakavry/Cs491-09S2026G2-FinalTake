from datetime import datetime
from . import db


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    media_id = db.Column(db.String(50), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)   # movie | tv | game | book
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'media_id', 'media_type', name='uq_user_media'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'media_id': self.media_id,
            'media_type': self.media_type,
            'title': self.title,
            'image_url': self.image_url,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
        }
