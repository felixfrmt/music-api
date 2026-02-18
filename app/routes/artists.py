from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Artist

artists_bp = Blueprint('artists', __name__, url_prefix='/artists')


@artists_bp.route('', methods=['POST'])
def create_artist():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Field "name" is required'}), 400

    artist = Artist(
        name=data['name'],
        bio=data.get('bio')
    )
    db.session.add(artist)
    db.session.commit()

    return jsonify(artist.to_dict()), 201


@artists_bp.route('', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    return jsonify([a.to_dict() for a in artists])


@artists_bp.route('/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    data = artist.to_dict()
    data['albums'] = [album.to_dict() for album in artist.albums]
    data['owned_tracks'] = [track.to_dict() for track in artist.owned_tracks]
    return jsonify(data)