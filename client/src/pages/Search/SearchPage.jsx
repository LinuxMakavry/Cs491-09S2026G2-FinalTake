import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import MediaCard from '../../components/media/MediaCard';
import { ThemeContext } from '../../context/ThemeContext';
import './SearchPage.css';

// Mock data - will be replaced with API calls once backend is ready
const mockMediaData = [
  { id: 1, title: "The Matrix", type: "movie", rating: 4.5, imageUrl: null },
  { id: 2, title: "Dune", type: "book", rating: 4.8, imageUrl: null },
  { id: 3, title: "The Last of Us", type: "game", rating: 5.0, imageUrl: null },
  { id: 4, title: "Breaking Bad", type: "tv", rating: 4.9, imageUrl: null },
  { id: 5, title: "Inception", type: "movie", rating: 4.7, imageUrl: null },
  { id: 6, title: "1984", type: "book", rating: 4.6, imageUrl: null },
  { id: 7, title: "God of War", type: "game", rating: 4.8, imageUrl: null },
  { id: 8, title: "Stranger Things", type: "tv", rating: 4.5, imageUrl: null },
];

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [mediaResults, setMediaResults] = useState(mockMediaData);
  const navigate = useNavigate();
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });

  const handleSearch = (e) => {
    e.preventDefault();
    // Filter mock data based on search query and type
    let filtered = mockMediaData;

    if (searchQuery) {
      filtered = filtered.filter(media =>
        media.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedType !== 'all') {
      filtered = filtered.filter(media => media.type === selectedType);
    }

    setMediaResults(filtered);
  };

  const handleReset = () => {
    setSearchQuery('');
    setSelectedType('all');
    setMediaResults(mockMediaData);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleHomeClick = () => {
    navigate('/search');
  };

  return (
    <div className="search-page">
      <header className="search-header">
        <div className="header-content">
          <button 
            className="home-button"
            onClick={handleHomeClick}
            title="Go to Home"
          >
            <h1 className="site-title">
              <span className="star-icon">★</span>
              FinalTake
              <span className="star-icon">★</span>
            </h1>
            <p className="site-tagline">Share Your Entertainment Experience</p>
          </button>
          <div className="header-actions">
            <button 
              className="btn btn-theme" 
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? '☽' : '☀'}
            </button>
            {user ? (
              <>
                <span className="user-email">{user.email}</span>
                <button className="btn btn-secondary" onClick={handleLogout}>
                  Logout
                </button>
              </>
            ) : (
              <button 
                className="btn btn-primary" 
                onClick={() => navigate('/login')}
              >
                Login
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="search-container">
        <form className="search-form" onSubmit={handleSearch}>
          <div className="search-input-group">
            <input
              type="text"
              className="search-input"
              placeholder="Search for movies, books, games, TV shows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <select
              className="type-filter"
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              <option value="all">All Types</option>
              <option value="movie">Movies</option>
              <option value="tv">TV Shows</option>
              <option value="book">Books</option>
              <option value="game">Games</option>
            </select>
          </div>
          <div className="search-buttons">
            <button type="submit" className="btn btn-primary">Search</button>
            <button type="button" className="btn btn-secondary" onClick={handleReset}>
              Reset
            </button>
          </div>
        </form>
      </div>

      <div className="results-container">
        <div className="results-header">
          <h2>
            {mediaResults.length === mockMediaData.length
              ? 'Browse Media'
              : `Search Results (${mediaResults.length})`}
          </h2>
        </div>

        {mediaResults.length > 0 ? (
          <div className="media-grid">
            {mediaResults.map((media) => (
              <MediaCard
                key={media.id}
                id={media.id}
                title={media.title}
                type={media.type}
                rating={media.rating}
                imageUrl={media.imageUrl}
              />
            ))}
          </div>
        ) : (
          <div className="no-results">
            <p>No media found matching your search.</p>
            <button className="btn btn-secondary" onClick={handleReset}>
              Clear Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
