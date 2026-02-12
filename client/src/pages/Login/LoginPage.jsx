import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');

    // Basic validation
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email');
      return;
    }

    // Store user in localStorage (basic session, no backend yet)
    localStorage.setItem('user', JSON.stringify({ email, isLoggedIn: true }));
    
    // Redirect to search page
    navigate('/search');
  };

  const handleHomeClick = () => {
    navigate('/search');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
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
          </button>
          <p className="site-tagline">Share Your Entertainment Experience</p>
        </div>

        <form className="login-form" onSubmit={handleLogin}>
          <h2>Login</h2>
          
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              className="form-input"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              className="form-input"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Login
          </button>
        </form>

        <p className="login-footer">
          Note: This is a basic login without backend. Any email/password will work for testing.
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
