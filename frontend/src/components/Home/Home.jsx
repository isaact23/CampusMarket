import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './Home.css'
import Toolbar from "./Toolbar/Toolbar.jsx"
import Content from "./Content/Content.jsx"
import Listings from "./Listings/Listings.jsx"

function Home() {
  return (
    <div className="home">
      <Toolbar />
      <Routes>
        <Route path="/" element={<Content />} />
        <Route path="/listings" element={<Listings />} />
      </Routes>
    </div>
  )
}

export default Home
