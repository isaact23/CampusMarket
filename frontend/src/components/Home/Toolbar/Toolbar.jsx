import SearchBox from "./SearchBox/SearchBox.jsx"
import { AuthContext } from "../../../contexts/AuthContext.jsx"
import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'

import './Toolbar.css'

const Toolbar = () => {
    const { authApi } = useContext(AuthContext)
    
    const navigate = useNavigate()
    
    const logout = () => {
        authApi.logout()
        navigate('/login')
    }
    const openListings = () => {
        navigate('/home/listings')
    }
    const openHome = () => {
        navigate('/home')
    }

    return (
        <div className="toolbar">
            <nav className="nav-bar">
                <div onClick={openHome} className="nav-logo">CampusMarket</div>
                <div className="nav-links">
                    <p className="nav-token">Token {token}</p>
                    <SearchBox />
                    <button onClick={openHome} className="nav-button">Home</button>
                    <button onClick={openListings} className="nav-button">Listings</button>
                    <button onClick={logout} className="nav-button">Log Out</button>
                </div>
            </nav>
        </div>
    )
}

export default Toolbar
