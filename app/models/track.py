from datetime import datetime
from ..extensions import db

# Association table: a track can have multiple featured artists
track_artists = db.Table(
    'track_artists',
    db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)


class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # The one artist who owns this track
    owner_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    # Optional: null = standalone track (not part of an album)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)

    # Featured artists (many-to-many)
    featured_artists = db.relationship(
        'Artist',
        secondary=track_artists,
        lazy='subquery',
        backref=db.backref('featured_on', lazy=True)
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'duration_seconds': self.duration_seconds,
            'owner_id': self.owner_id,
            'album_id': self.album_id,
            'featured_artist_ids': [a.id for a in self.featured_artists],
            'created_at': self.created_at.isoformat()
        }