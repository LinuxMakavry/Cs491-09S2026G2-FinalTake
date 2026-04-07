import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThemeContext } from '../../context/ThemeContext';
import '../../styles/ProfilePage.css';

const ProfilePage = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleHomeClick = () => {
    navigate('/search');
  };

  if (!user) {
    navigate('/login');
    return null;
  }

  const memberSince = user.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
    : 'Unknown';

  return (
    <div className="profile-page">
      <header className="profile-header">
        <div className="header-content">
          <button className="home-button" onClick={handleHomeClick} title="Go to Home">
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
            <button className="btn btn-secondary" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="profile-content">
        {/* User Info Card */}
        <div className="profile-card">
          <div className="profile-avatar">
            <span className="avatar-initials">
              {user.username ? user.username[0].toUpperCase() : '?'}
            </span>
          </div>
          <div className="profile-info">
            <h2 className="profile-username">{user.username}</h2>
            <p className="profile-email">{user.email}</p>
            <p className="profile-since">Member since {memberSince}</p>
          </div>
        </div>

        {/* Stats Row */}
        <div className="profile-stats">
          <div className="stat-card">
            <span className="stat-number">0</span>
            <span className="stat-label">Favorites</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">0</span>
            <span className="stat-label">Reviews</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">0</span>
            <span className="stat-label">Ratings</span>
          </div>
        </div>

        {/* Favorites Section */}
        <section className="profile-section">
          <h3 className="section-title">❤ Favorites</h3>
          <div className="section-empty">
            <p>No favorites yet.</p>
            <button className="btn btn-primary" onClick={handleHomeClick}>
              Browse Media
            </button>
          </div>
        </section>

        {/* Reviews Section */}
        <section className="profile-section">
          <h3 className="section-title">✏ Reviews</h3>
          <div className="section-empty">
            <p>No reviews yet.</p>
            <button className="btn btn-primary" onClick={handleHomeClick}>
              Browse Media
            </button>
          </div>
        </section>

        {/* Ratings Section */}
        <section className="profile-section">
          <h3 className="section-title">★ Ratings</h3>
          <div className="section-empty">
            <p>No ratings yet.</p>
            <button className="btn btn-primary" onClick={handleHomeClick}>
              Browse Media
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ProfilePage;
