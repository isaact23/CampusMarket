import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login/Login.jsx';
import Register from './Register/Register.jsx';
import Home from './Home/Home.jsx'
import ConnectionTest from './ConnectionTest/ConnectionTest.jsx';
import { TokenProvider } from './TokenProvider.jsx'
import NotFound from './NotFound/NotFound.jsx';

const App = () => {
  return (
    <TokenProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/home*" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/test-api" element={<ConnectionTest />} />
          <Route path="*" element={<NotFound />} /> {/* This catches all undefined routes */}
        </Routes>
      </Router>
    </TokenProvider>
  )
}
export default App
