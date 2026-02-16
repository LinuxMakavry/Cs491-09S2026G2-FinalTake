import { useNavigate } from 'react-router-dom';
import '../styles/MediaCard.css';

const MediaCard = ({ id, title, type, rating, imageUrl }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/media/${id}`);
  };

  // Function to render stars based on rating
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

  return (
    <div className="media-card" onClick={handleClick}>
      <div className="media-image">
        {imageUrl ? (
          <img src={imageUrl} alt={title} />
        ) : (
          <div className="placeholder-image">
            <span>No Image</span>
          </div>
        )}
      </div>
      <div className="media-info">
        <h3 className="media-title">{title}</h3>
        <span className="media-type">{type}</span>
        <div className="media-rating">
          {renderStars(rating)}
          <span className="rating-value">{rating.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

export default MediaCard;
