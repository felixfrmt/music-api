from datetime import datetime
from ..extensions import db


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    # One album → many tracks
    tracks = db.relationship('Track', backref='album', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'cover_url': self.cover_url,
            'artist_id': self.artist_id,
            'created_at': self.created_at.isoformat()
        }