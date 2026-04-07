import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect, useCallback } from 'react';
import '../../styles/MediaDetailsPage.css';

const MediaDetailsPage = () => {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const [media, setMedia] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const authHeaders = user ? { 'X-User-Id': String(user.id) } : {};

  useEffect(() => {
    const fetchDetails = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const res = await fetch(`/api/media/${type}/${id}`);
        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.error || `Server error ${res.status}`);
        }
        const data = await res.json();
        setMedia(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDetails();
  }, [type, id]);

  // Check favorite status once media is loaded
  useEffect(() => {
    if (!user || !id || !type) return;
    fetch(`/api/favorites/check/${type}/${id}`, { headers: authHeaders })
      .then(r => r.json())
      .then(data => setIsFavorite(data.is_favorite))
      .catch(() => {});
  }, [id, type]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleFavoriteToggle = useCallback(async () => {
    if (!user) { navigate('/login'); return; }
    setFavoriteLoading(true);
    try {
      if (isFavorite) {
        await fetch(`/api/favorites/${type}/${id}`, {
          method: 'DELETE',
          headers: authHeaders,
        });
        setIsFavorite(false);
      } else {
        await fetch('/api/favorites', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...authHeaders },
          body: JSON.stringify({
            media_id: id,
            media_type: type,
            title: media?.title || '',
            image_url: media?.imageUrl || null,
            rating: media?.rating || null,
          }),
        });
        setIsFavorite(true);
      }
    } catch {
      // silently ignore network errors
    } finally {
      setFavoriteLoading(false);
    }
  }, [isFavorite, id, type, media, user]); // eslint-disable-line react-hooks/exhaustive-deps

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={`full-${i}`} className="star full">★</span>);
    }

    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">☆</span>);
    }

    return stars;
  };

  const getCreatorLabel = (type) => {
    return type === 'movie' ? 'Director' : 'Creator';
  };

  const getCreatorValue = (media) => {
    return media.director || media.creator || 'Unknown';
  };

  if (isLoading) {
    return (
      <div className="media-details-page">
        <div className="loading-container">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error || !media) {
    return (
      <div className="media-details-page">
        <div className="error-container">
          <h2>Media Not Found</h2>
          <p>{error || 'The requested media could not be found.'}</p>
          <button className="btn btn-primary" onClick={() => navigate('/search')}>
            Back to Search
          </button>
        </div>
      </div>
    );
  }
  return (
    <div className="media-details-page">
      <button className="back-button" onClick={() => navigate('/search')}>
        ← Back to Search
      </button>

      <div className="details-container">
        <div className="details-header">
          <div className="media-image-large">
            {media.imageUrl ? (
              <img src={media.imageUrl} alt={media.title} />
            ) : (
              <div className="placeholder-image-large">
                <span className="placeholder-icon">🎬</span>
              </div>
            )}
          </div>

          <div className="media-info-section">
            <div className="type-badge">{media.type}</div>
            <h1 className="media-title-large">{media.title}</h1>
            <div className="media-meta">
              <span className="meta-item">{media.releaseYear}</span>
              <span className="meta-separator">•</span>
              <span className="meta-item">{getCreatorLabel(media.type)}: {getCreatorValue(media)}</span>
            </div>
            
            <div className="rating-section">
              <div className="stars-display">
                {renderStars(media.rating)}
              </div>
              <span className="rating-number">{media.rating.toFixed(1)} / 5.0</span>
            </div>

            <div className="genre-tags">
              {media.genre.map((g, index) => (
                <span key={index} className="genre-tag">{g}</span>
              ))}
            </div>

            <button
              className={`favorite-button ${isFavorite ? 'favorited' : ''}`}
              onClick={handleFavoriteToggle}
              disabled={favoriteLoading}
            >
              <span className="heart-icon">{isFavorite ? '❤️' : '🤍'}</span>
              {favoriteLoading ? 'Saving...' : isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
            </button>
          </div>
        </div>
        <div className="details-body">
          <section className="description-section">
            <h2>Description</h2>
            <p>{media.description}</p>
          </section>

          <section className="reviews-section">
            <h2>Reviews</h2>
            <div className="reviews-placeholder">
              <p>No reviews yet. Be the first to review!</p>
              <button className="btn btn-primary" disabled>
                Write a Review (Coming Soon)
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default MediaDetailsPage;