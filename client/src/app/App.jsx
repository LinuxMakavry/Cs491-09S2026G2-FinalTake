import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SearchPage from '../pages/Search/SearchPage';
import MediaDetailsPage from '../pages/MediaDetails/MediaDetailsPage';
import LoginPage from '../pages/Login/LoginPage';
import { ThemeProvider } from '../context/ThemeContext';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Default route redirects to search */}
            <Route path="/" element={<Navigate to="/search" replace />} />
            
            {/* Login page */}
            <Route path="/login" element={<LoginPage />} />
            
            {/* Search page - main landing */}
            <Route path="/search" element={<SearchPage />} />
            
            {/* Media details page */}
            <Route path="/media/:id" element={<MediaDetailsPage />} />
            
            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/search" replace />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
