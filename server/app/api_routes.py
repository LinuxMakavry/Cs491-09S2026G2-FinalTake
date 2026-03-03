"""API routes that query TMDB as database"""
from flask import Blueprint, request, jsonify
from app.tmdb_service import TMDBService

bp = Blueprint('api', __name__, url_prefix='/api')
tmdb = TMDBService()


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'FinalTake API is running'}), 200


@bp.route('/search', methods=['GET'])
def search():
    """
    Search for movies, TV shows, or both
    Query params:
    - q: search query (required)
    - type: 'movie', 'tv', or 'multi' (default: 'multi')
    - page: page number (default: 1)
    """
    query = request.args.get('query') or request.args.get('q')
    media_type = request.args.get('type', 'multi')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400
    
    if media_type == 'all':
        media_type = 'multi'
    
    if media_type not in ['movie', 'tv', 'multi']:
        return jsonify({'error': 'Type must be "movie", "tv", or "multi"'}), 400
    
    results = tmdb.search_media(query, media_type, page)
    
    if results is None:
        return jsonify({'error': 'Failed to fetch from TMDB API'}), 500
    
    return jsonify(results), 200


@bp.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get movie details from TMDB"""
    movie = tmdb.get_movie(movie_id)
    
    if movie is None:
        return jsonify({'error': 'Failed to fetch movie details'}), 500
    
    if 'success' in movie and not movie['success']:
        return jsonify({'error': 'Movie not found'}), 404
    
    return jsonify(movie), 200


@bp.route('/tv/<int:tv_id>', methods=['GET'])
def get_tv(tv_id):
    """Get TV show details from TMDB"""
    tv = tmdb.get_tv(tv_id)
    
    if tv is None:
        return jsonify({'error': 'Failed to fetch TV show details'}), 500
    
    if 'success' in tv and not tv['success']:
        return jsonify({'error': 'TV show not found'}), 404
    
    return jsonify(tv), 200


@bp.route('/genres', methods=['GET'])
def get_genres():
    """Get list of genres"""
    media_type = request.args.get('type', 'movie')
    
    if media_type not in ['movie', 'tv']:
        return jsonify({'error': 'Type must be "movie" or "tv"'}), 400
    
    genres = tmdb.get_genres(media_type)
    
    if genres is None:
        return jsonify({'error': 'Failed to fetch genres'}), 500
    
    return jsonify(genres), 200


@bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending movies/shows"""
    media_type = request.args.get('type', 'movie')
    time_window = request.args.get('window', 'week')
    
    if media_type not in ['movie', 'tv']:
        return jsonify({'error': 'Type must be "movie" or "tv"'}), 400
    
    if time_window not in ['day', 'week']:
        return jsonify({'error': 'Window must be "day" or "week"'}), 400
    
    trending = tmdb.get_trending(media_type, time_window)
    
    if trending is None:
        return jsonify({'error': 'Failed to fetch trending'}), 500
    
    return jsonify(trending), 200


@bp.route('/popular', methods=['GET'])
def get_popular():
    """Get popular movies/shows"""
    media_type = request.args.get('type', 'movie')
    page = request.args.get('page', 1, type=int)
    
    if media_type not in ['movie', 'tv']:
        return jsonify({'error': 'Type must be "movie" or "tv"'}), 400
    
    popular = tmdb.get_popular(media_type, page)
    
    if popular is None:
        return jsonify({'error': 'Failed to fetch popular media'}), 500
    
    return jsonify(popular), 200


@bp.route('/top-rated', methods=['GET'])
def get_top_rated():
    """Get top rated movies/shows"""
    media_type = request.args.get('type', 'movie')
    page = request.args.get('page', 1, type=int)
    
    if media_type not in ['movie', 'tv']:
        return jsonify({'error': 'Type must be "movie" or "tv"'}), 400
    
    top_rated = tmdb.get_top_rated(media_type, page)
    
    if top_rated is None:
        return jsonify({'error': 'Failed to fetch top rated media'}), 500
    
    return jsonify(top_rated), 200


@bp.route('/media/<media_type>/<int:media_id>', methods=['GET'])
def get_media_details(media_type, media_id):
    """Get details for a movie or TV show by type and ID"""
    if media_type == 'movie':
        data = tmdb.get_movie(media_id)
    elif media_type == 'tv':
        data = tmdb.get_tv(media_id)
    else:
        return jsonify({'error': 'media_type must be "movie" or "tv"'}), 400

    if data is None:
        return jsonify({'error': 'Failed to fetch media details'}), 500

    return jsonify(data), 200
