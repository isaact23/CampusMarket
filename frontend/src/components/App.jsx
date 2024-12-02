import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login/Login.jsx';
import Register from './Register/Register.jsx';
import Home from './Home/Home.jsx'
import ConnectionTest from './ConnectionTest/ConnectionTest.jsx';
import { useBackgroundColor } from '../contexts/BackgroundColorContext.jsx'
import NotFound from './NotFound/NotFound.jsx';


const App = () => {
  const color = useBackgroundColor();

  return (
    <div style={{background: color, height: '100vh'}}>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/home/*" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/test-api" element={<ConnectionTest />} />
        <Route path="*" element={<NotFound />} /> {/* This catches all undefined routes */}
      </Routes>
    </div>
  )
}
export default App
