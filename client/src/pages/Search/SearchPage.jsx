import { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MediaCard from '../../components/media/MediaCard';
import { ThemeContext } from '../../context/ThemeContext';
import '../../styles/SearchPage.css';

const SkeletonCard = () => (
  <div className="skeleton-card">
    <div className="skeleton-image" />
    <div className="skeleton-text skeleton-title" />
    <div className="skeleton-text skeleton-subtitle" />
  </div>
);

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [mediaResults, setMediaResults] = useState([]);
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [trendingShows, setTrendingShows] = useState([]);
  const [trendingGames, setTrendingGames] = useState([]);
  const [trendingBooks, setTrendingBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTrendingLoading, setIsTrendingLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [activeTab, setActiveTab] = useState('movies');
  const navigate = useNavigate();
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });

  // Fetch trending on mount
  useEffect(() => {
    const fetchTrending = async () => {
      setIsTrendingLoading(true);
      try {
        const response = await fetch('/api/trending-all').then(r => r.json());
        setTrendingMovies(response.movies || []);
        setTrendingShows(response.shows || []);
        setTrendingGames(response.games || []);
        setTrendingBooks(response.books || []);
      } catch {
        setTrendingMovies([]);
        setTrendingShows([]);
        setTrendingGames([]);
        setTrendingBooks([]);
      } finally {
        setIsTrendingLoading(false);
      }
    };
    fetchTrending();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const params = new URLSearchParams({ query: searchQuery.trim() });
      if (selectedType !== 'all') params.append('type', selectedType);

      const res = await fetch(`/api/search?${params}`);
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || `Server error ${res.status}`);
      }
      const data = await res.json();
      setMediaResults(data.results || []);
    } catch (err) {
      setError(err.message);
      setMediaResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSearchQuery('');
    setSelectedType('all');
    setMediaResults([]);
    setHasSearched(false);
    setError(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleHomeClick = () => {
    navigate('/search');
  };

  const trendingTabs = [
    { key: 'movies', label: 'Movies', data: trendingMovies },
    { key: 'tv', label: 'TV Shows', data: trendingShows },
    { key: 'games', label: 'Games', data: trendingGames },
    { key: 'books', label: 'Books', data: trendingBooks },
  ];

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
              <option value="game">Games</option>
              <option value="book">Books</option>
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
        {error && (
          <div className="error-state">
            <p>Error: {error}</p>
          </div>
        )}

        {!error && hasSearched && (
          <>
            <div className="results-header">
              <h2>Search Results {!isLoading && `(${mediaResults.length})`}</h2>
            </div>
            {isLoading ? (
              <div className="media-grid">
                {Array.from({ length: 8 }, (_, i) => <SkeletonCard key={i} />)}
              </div>
            ) : mediaResults.length > 0 ? (
              <div className="media-grid">
                {mediaResults.map((media) => (
                  <MediaCard
                    key={`${media.type}-${media.id}`}
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
          </>
        )}

        {!error && !hasSearched && (
          <>
            <div className="trending-tabs">
              {trendingTabs.map(({ key, label }) => (
                <button
                  key={key}
                  className={`tab-btn${activeTab === key ? ' tab-btn--active' : ''}`}
                  onClick={() => setActiveTab(key)}
                  disabled={isTrendingLoading}
                >
                  {label}
                </button>
              ))}
            </div>
            {isTrendingLoading ? (
              <div className="media-grid">
                {Array.from({ length: 8 }, (_, i) => <SkeletonCard key={i} />)}
              </div>
            ) : (
              trendingTabs.map(({ key, label, data }) =>
                activeTab === key && (
                  <div key={key}>
                    <div className="results-header">
                      <h2>Trending {label}</h2>
                    </div>
                    <div className="media-grid">
                      {data.map((media) => (
                        <MediaCard
                          key={`${key}-${media.id}`}
                          id={media.id}
                          title={media.title}
                          type={media.type}
                          rating={media.rating}
                          imageUrl={media.imageUrl}
                        />
                      ))}
                    </div>
                  </div>
                )
              )
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
