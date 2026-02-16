import { useParams, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import '../../styles/MediaDetailsPage.css';

const mockMediaDetails = {
  1: {
    id: 1,
    title: "The Matrix",
    type: "movie",
    rating: 4.5,
    releaseYear: 1999,
    director: "The Wachowskis",
    description: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    genre: ["Sci-Fi", "Action"],
    imageUrl: null
  },
  2: {
    id: 2,
    title: "Dune",
    type: "book",
    rating: 4.8,
    releaseYear: 1965,
    author: "Frank Herbert",
    description: "Set in the distant future amidst a feudal interstellar society, Dune tells the story of young Paul Atreides.",
    genre: ["Sci-Fi", "Fantasy"],
    imageUrl: null
  },
  3: {
    id: 3,
    title: "The Last of Us",
    type: "game",
    rating: 5.0,
    releaseYear: 2013,
    developer: "Naughty Dog",
    description: "Joel and Ellie must survive a brutal journey across a post-pandemic United States.",
    genre: ["Action", "Adventure", "Survival"],
    imageUrl: null
  },
  4: {
    id: 4,
    title: "Breaking Bad",
    type: "tv",
    rating: 4.9,
    releaseYear: 2008,
    creator: "Vince Gilligan",
    description: "A chemistry teacher turns to manufacturing methamphetamine to secure his family's future.",
    genre: ["Crime", "Drama", "Thriller"],
    imageUrl: null
  },
  
  5: {
    id: 5,
    title: "Inception",
    type: "movie",
    rating: 4.7,
    releaseYear: 2010,
    director: "Christopher Nolan",
    description: "A thief who steals corporate secrets through dream-sharing technology.",
    genre: ["Sci-Fi", "Thriller"],
    imageUrl: null
  },
  6: {
    id: 6,
    title: "1984",
    type: "book",
    rating: 4.6,
    releaseYear: 1949,
    author: "George Orwell",
    description: "A dystopian novel following Winston Smith in a totalitarian society.",
    genre: ["Dystopian", "Political Fiction"],
    imageUrl: null
  },
  7: {
    id: 7,
    title: "God of War",
    type: "game",
    rating: 4.8,
    releaseYear: 2018,
    developer: "Santa Monica Studio",
    description: "Kratos and Atreus journey through Norse mythology.",
    genre: ["Action", "Adventure"],
    imageUrl: null
  },
  8: {
    id: 8,
    title: "Stranger Things",
    type: "tv",
    rating: 4.5,
    releaseYear: 2016,
    creator: "The Duffer Brothers",
    description: "A group must confront supernatural forces to find a missing boy.",
    genre: ["Sci-Fi", "Horror", "Drama"],
    imageUrl: null
  }
};

const MediaDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [isFavorite, setIsFavorite] = useState(false);

  const media = mockMediaDetails[id];

  if (!media) {
    return (
      <div className="media-details-page">
        <div className="error-container">
          <h2>Media Not Found</h2>
          <p>The requested media could not be found.</p>
          <button className="btn btn-primary" onClick={() => navigate('/search')}>
            Back to Search
          </button>
        </div>
      </div>
    );
  }

  const handleFavoriteToggle = () => {
    setIsFavorite(!isFavorite);
  };

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
    switch (type) {
      case 'movie': return 'Director';
      case 'tv': return 'Creator';
      case 'book': return 'Author';
      case 'game': return 'Developer';
      default: return 'Creator';
    }
  };

  const getCreatorValue = (media) => {
    return media.director || media.creator || media.author || media.developer || 'Unknown';
  };
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
            >
              <span className="heart-icon">{isFavorite ? '❤️' : '🤍'}</span>
              {isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
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