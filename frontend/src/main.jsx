// frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from "./components/App.jsx"
import {TokenProvider} from "./contexts/TokenContext.jsx"
import { BackgroundColorProvider } from './contexts/BackgroundColorContext.jsx';
import { BrowserRouter as Router } from 'react-router-dom';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <TokenProvider>
        <BackgroundColorProvider>
          <App />
        </BackgroundColorProvider>
      </TokenProvider>
    </Router>
  </StrictMode>
);