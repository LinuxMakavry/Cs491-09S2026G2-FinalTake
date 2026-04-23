from flask import Blueprint, request, jsonify
from app.models import db
from app.models.favorite import Favorite
from app.models.user import User

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')


def _get_user(request):
    """Extract user_id from the X-User-Id header sent by the frontend."""
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        return None, jsonify({'error': 'Authentication required'}), 401
    user = User.query.get(user_id)
    if not user:
        return None, jsonify({'error': 'User not found'}), 404
    return user, None, None


@favorites_bp.route('', methods=['GET'])
def get_favorites():
    """Return all favorites for the authenticated user."""
    user, err_response, status = _get_user(request)
    if err_response:
        return err_response, status

    favorites = Favorite.query.filter_by(user_id=user.id).order_by(Favorite.created_at.desc()).all()
    return jsonify({'favorites': [f.to_dict() for f in favorites]}), 200


@favorites_bp.route('', methods=['POST'])
def add_favorite():
    """Add a media item to the user's favorites."""
    user, err_response, status = _get_user(request)
    if err_response:
        return err_response, status

    data = request.get_json()
    if not data or not data.get('media_id') or not data.get('media_type') or not data.get('title'):
        return jsonify({'error': 'media_id, media_type, and title are required'}), 400

    # Prevent duplicates
    existing = Favorite.query.filter_by(
        user_id=user.id,
        media_id=str(data['media_id']),
        media_type=data['media_type']
    ).first()
    if existing:
        return jsonify({'favorite': existing.to_dict(), 'message': 'Already in favorites'}), 200

    favorite = Favorite(
        user_id=user.id,
        media_id=str(data['media_id']),
        media_type=data['media_type'],
        title=data['title'],
        image_url=data.get('image_url'),
        rating=data.get('rating'),
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'favorite': favorite.to_dict(), 'message': 'Added to favorites'}), 201


@favorites_bp.route('/<string:media_type>/<string:media_id>', methods=['DELETE'])
def remove_favorite(media_type, media_id):
    """Remove a media item from the user's favorites."""
    user, err_response, status = _get_user(request)
    if err_response:
        return err_response, status

    favorite = Favorite.query.filter_by(
        user_id=user.id,
        media_id=media_id,
        media_type=media_type
    ).first()
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Removed from favorites'}), 200


@favorites_bp.route('/check/<string:media_type>/<string:media_id>', methods=['GET'])
def check_favorite(media_type, media_id):
    """Check whether a specific media item is in the user's favorites."""
    user, err_response, status = _get_user(request)
    if err_response:
        return err_response, status

    exists = Favorite.query.filter_by(
        user_id=user.id,
        media_id=media_id,
        media_type=media_type
    ).first() is not None
    return jsonify({'is_favorite': exists}), 200
