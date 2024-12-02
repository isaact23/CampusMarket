import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './Home.css'
import Toolbar from "./Toolbar/Toolbar.jsx"
import Content from "./Content/Content.jsx"

function Home() {
    return (
        <Router>
            <Routes>
                <div className="home">
                    <Toolbar />
                    <Route path="/" element={<Content />} />
                    <Route path="/listings" element={<Listings />} />
                    <Content />
                </div>
            </Routes>
        </Router>
    )
}

export default Home
