from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Artist, Album, Track

tracks_bp = Blueprint('tracks', __name__, url_prefix='/tracks')


@tracks_bp.route('', methods=['POST'])
def create_track():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('owner_id'):
        return jsonify({'error': 'Fields "title" and "owner_id" are required'}), 400

    if not Artist.query.get(data['owner_id']):
        return jsonify({'error': f'Artist with id {data["owner_id"]} not found'}), 404

    if data.get('album_id') and not Album.query.get(data['album_id']):
        return jsonify({'error': f'Album with id {data["album_id"]} not found'}), 404

    track = Track(
        title=data['title'],
        owner_id=data['owner_id'],
        album_id=data.get('album_id'),
        duration_seconds=data.get('duration_seconds')
    )

    # Add featured artists (optional)
    for artist_id in data.get('featured_artist_ids', []):
        artist = Artist.query.get(artist_id)
        if not artist:
            return jsonify({'error': f'Featured artist with id {artist_id} not found'}), 404
        track.featured_artists.append(artist)

    db.session.add(track)
    db.session.commit()

    return jsonify(track.to_dict()), 201


@tracks_bp.route('', methods=['GET'])
def get_tracks():
    tracks = Track.query.all()
    return jsonify([t.to_dict() for t in tracks])


@tracks_bp.route('/<int:track_id>', methods=['GET'])
def get_track(track_id):
    track = Track.query.get_or_404(track_id)
    return jsonify(track.to_dict())