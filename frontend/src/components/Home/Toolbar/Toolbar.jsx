import SearchBox from "./SearchBox/SearchBox.jsx"
import {TokenContext} from "../../../contexts/TokenContext.jsx"
import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'

import './Toolbar.css'

const Toolbar = () => {
    const {token, setToken} = useContext(TokenContext)
    
    const navigate = useNavigate()
    
    const logout = () => {
        setToken(null)
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
            <div className="home-header w3-bar w3-card-4 w3-theme-d3 w3-top">
                <h2 className="w3-bar-item w3-left">CampusMarket</h2>
                <p className="w3-bar-item w3-left w3-white">Token {token}</p>
                <a className="w3-bar-item w3-button w3-right" onClick={logout}><h2>Log Out</h2></a>
                <a className="w3-bar-item w3-button w3-right" onClick={openListings}><h2>Listings</h2></a>
                <a className="w3-bar-item w3-button w3-right" onClick={openHome}><h2>Home</h2></a>
                <div className="w3-bar-item w3-right w3-margin">
                    <SearchBox />
                </div>
            </div>
        </div>
    )
}

export default Toolbar
