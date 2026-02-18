from datetime import datetime
from ..extensions import db


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One artist → many albums
    albums = db.relationship('Album', backref='artist', lazy=True)
    # Tracks owned by this artist
    owned_tracks = db.relationship(
        'Track', backref='owner', lazy=True, foreign_keys='Track.owner_id'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'created_at': self.created_at.isoformat()
        }