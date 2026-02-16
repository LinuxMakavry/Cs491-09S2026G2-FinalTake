import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
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
      <header className="login-header">
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
      </header>

      <div className="login-container">
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
            <div className="password-input-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                className="form-input"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowPassword(!showPassword)}
                title={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? 'HIDE' : 'SHOW'}
              </button>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-full">
            Login
          </button>

          <div className="forgot-password-section">
            <button type="button" className="forgot-password-link">
              Forgot your password?
            </button>
          </div>
        </form>

        <div className="signup-section">
          <p className="signup-text">Don't have an account? <button className="signup-link">Sign up</button></p>
        </div>

        <p className="login-footer">
          Note: This is a basic login without backend. Any email/password will work for testing as long as the email contains '@' i.e. test@test.com
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
