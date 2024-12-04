// frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from "./components/App.jsx"
import { AuthProvider } from "./contexts/AuthContext.jsx"
import { BackgroundColorProvider } from './contexts/BackgroundColorContext.jsx';
import { BrowserRouter as Router } from 'react-router-dom';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <AuthProvider>
        <BackgroundColorProvider>
          <App />
        </BackgroundColorProvider>
      </AuthProvider>
    </Router>
  </StrictMode>
);