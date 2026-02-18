from flask import Blueprint, request, jsonify
from datetime import datetime
from ..extensions import db
from ..models import Artist, Album

albums_bp = Blueprint('albums', __name__, url_prefix='/albums')


@albums_bp.route('', methods=['POST'])
def create_album():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('artist_id'):
        return jsonify({'error': 'Fields "title" and "artist_id" are required'}), 400

    if not Artist.query.get(data['artist_id']):
        return jsonify({'error': f'Artist with id {data["artist_id"]} not found'}), 404

    release_date = None
    if data.get('release_date'):
        try:
            release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'release_date must be in YYYY-MM-DD format'}), 400

    album = Album(
        title=data['title'],
        artist_id=data['artist_id'],
        release_date=release_date,
        cover_url=data.get('cover_url')
    )
    db.session.add(album)
    db.session.commit()

    return jsonify(album.to_dict()), 201


@albums_bp.route('', methods=['GET'])
def get_albums():
    albums = Album.query.all()
    return jsonify([a.to_dict() for a in albums])


@albums_bp.route('/<int:album_id>', methods=['GET'])
def get_album(album_id):
    album = Album.query.get_or_404(album_id)
    data = album.to_dict()
    data['tracks'] = [track.to_dict() for track in album.tracks]
    return jsonify(data)