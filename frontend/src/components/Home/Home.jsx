import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react'
import './Home.css'
import Toolbar from "./Toolbar/Toolbar.jsx"
import Content from "./Content/Content.jsx"
import Listings from "./Listings/Listings.jsx"
import { AuthContext } from "../../contexts/AuthContext.jsx"

function Home() {
  const { authApi } = useContext(AuthContext)

  return (
    <div className="home">
      {authApi.getIsLoggedIn() ? '' : <Navigate to="/login" />}
      <Toolbar />
      <Routes>
        <Route path="/" element={<Content />} />
        <Route path="/listings" element={<Listings />} />
      </Routes>
    </div>
  )
}

export default Home
