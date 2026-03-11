import requests
from flask import Blueprint, jsonify, request, current_app

tmdb_bp = Blueprint('tmdb', __name__)


def _tmdb_get(path, params=None):
    """Make an authenticated GET request to the TMDB v3 API."""
    base_url = current_app.config['TMDB_BASE_URL']
    api_key = current_app.config['TMDB_API_KEY']
    params = params or {}
    params['api_key'] = api_key
    response = requests.get(f"{base_url}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def _format_result(item, media_type=None):
    """Normalise a TMDB result into the shape the frontend expects."""
    image_base = current_app.config['TMDB_IMAGE_BASE']
    mtype = media_type or item.get('media_type', 'movie')
    poster = item.get('poster_path')
    return {
        'id': item.get('id'),
        'title': item.get('title') or item.get('name', 'Unknown'),
        'type': mtype,
        'rating': round(item.get('vote_average', 0) / 2, 1),  # TMDB 0-10 → 0-5
        'imageUrl': f"{image_base}{poster}" if poster else None,
        'releaseYear': (item.get('release_date') or item.get('first_air_date') or '')[:4] or None,
        'overview': item.get('overview', ''),
        'genres': item.get('genre_ids', []),
    }


# ---------------------------------------------------------------------------
# POST /api/search  (or GET with query params)
# ---------------------------------------------------------------------------
@tmdb_bp.route('/search', methods=['GET'])
def search():
    """Search TMDB for movies and/or TV shows.

    Query params:
        query (str)  – search term (required)
        type  (str)  – 'movie' | 'tv' | 'all'  (default: 'all')
        page  (int)  – page number (default: 1)
    """
    query = request.args.get('query', '').strip()
    media_type = request.args.get('type', 'all').lower()
    page = request.args.get('page', 1)

    if not query:
        return jsonify({'error': 'query parameter is required'}), 400

    try:
        if media_type == 'all':
            data = _tmdb_get('/search/multi', {'query': query, 'page': page})
            results = [
                _format_result(r)
                for r in data.get('results', [])
                if r.get('media_type') in ('movie', 'tv')
            ]
        elif media_type in ('movie', 'tv'):
            data = _tmdb_get(f'/search/{media_type}', {'query': query, 'page': page})
            results = [_format_result(r, media_type) for r in data.get('results', [])]
        else:
            return jsonify({'error': f"Unknown type '{media_type}'. Use 'movie', 'tv', or 'all'."}), 400

        return jsonify({
            'results': results,
            'totalResults': data.get('total_results', len(results)),
            'totalPages': data.get('total_pages', 1),
            'page': data.get('page', 1),
        })

    except requests.HTTPError as e:
        return jsonify({'error': f'TMDB error: {e.response.status_code}'}), 502
    except requests.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 503


# ---------------------------------------------------------------------------
# GET /api/media/<media_type>/<id>
# ---------------------------------------------------------------------------
@tmdb_bp.route('/media/<media_type>/<int:media_id>', methods=['GET'])
def media_details(media_type, media_id):
    """Fetch full details for a single movie or TV show.

    Params:
        media_type – 'movie' or 'tv'
        media_id   – TMDB integer ID
    """
    if media_type not in ('movie', 'tv'):
        return jsonify({'error': "media_type must be 'movie' or 'tv'"}), 400

    image_base = current_app.config['TMDB_IMAGE_BASE']

    try:
        # Fetch details + credits in parallel via append_to_response
        data = _tmdb_get(
            f'/{media_type}/{media_id}',
            {'append_to_response': 'credits'}
        )

        poster = data.get('poster_path')
        backdrop = data.get('backdrop_path')

        genres = [g['name'] for g in data.get('genres', [])]

        # Extract creator/director
        credits = data.get('credits', {})
        director = None
        creator = None
        if media_type == 'movie':
            crew = credits.get('crew', [])
            directors = [p['name'] for p in crew if p.get('job') == 'Director']
            director = ', '.join(directors) if directors else None
        else:
            creators = data.get('created_by', [])
            creator = ', '.join(c['name'] for c in creators) if creators else None

        cast = [
            {'name': p['name'], 'character': p.get('character', '')}
            for p in credits.get('cast', [])[:10]
        ]

        release_year = (
            data.get('release_date') or data.get('first_air_date') or ''
        )[:4] or None

        return jsonify({
            'id': data.get('id'),
            'title': data.get('title') or data.get('name'),
            'type': media_type,
            'rating': round(data.get('vote_average', 0) / 2, 1),
            'releaseYear': release_year,
            'director': director,
            'creator': creator,
            'description': data.get('overview', ''),
            'genre': genres,
            'imageUrl': f"{image_base}{poster}" if poster else None,
            'backdropUrl': f"https://image.tmdb.org/t/p/original{backdrop}" if backdrop else None,
            'cast': cast,
            'runtime': data.get('runtime'),
            'tagline': data.get('tagline', ''),
            'voteCount': data.get('vote_count', 0),
        })

    except requests.HTTPError as e:
        status = e.response.status_code
        if status == 404:
            return jsonify({'error': 'Media not found on TMDB'}), 404
        return jsonify({'error': f'TMDB error: {status}'}), 502
    except requests.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 503
