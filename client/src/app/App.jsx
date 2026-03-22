import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SearchPage from '../pages/Search/SearchPage';
import MediaDetailsPage from '../pages/MediaDetails/MediaDetailsPage';
import LoginPage from '../pages/Login/LoginPage';
import { ThemeProvider } from '../context/ThemeContext';
import '../styles/App.css';

function PrivateRoute({ children }) {
  const user = localStorage.getItem('user');
  return user ? children : <Navigate to="/login" replace />;
}

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
            
            {/* Search page - protected */}
            <Route path="/search" element={<PrivateRoute><SearchPage /></PrivateRoute>} />
            
            {/* Media details page - protected */}
            <Route path="/media/:type/:id" element={<PrivateRoute><MediaDetailsPage /></PrivateRoute>} />
            
            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/search" replace />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
