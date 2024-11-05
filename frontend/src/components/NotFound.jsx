// frontend/src/components/NotFound.jsx
import { useNavigate } from 'react-router-dom';
import './NotFound.css';

function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="not-found-container">
      <div className="not-found-box">
        <h2>404</h2>
        <h3>Page Not Found</h3>
        <p>The page you're looking for doesn't exist.</p>
        <button 
          className="back-button"
          onClick={() => navigate('/login')}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}

export default NotFound;