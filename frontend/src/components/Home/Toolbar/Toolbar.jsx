import SearchBox from "./SearchBox/SearchBox.jsx"
import {TokenContext} from "../../TokenProvider.jsx"
import { useContext } from 'react'

const Toolbar = () => {
    const {token, setToken} = useContext(TokenContext)
    
    const logout = () => {
        setToken(null)
        window.location = '/login'
    }

    return (
        <div className="toolbar">
            <div className="home-header w3-bar w3-card-4 w3-theme-d3 w3-top">
                <h2 className="w3-bar-item w3-left">CampusMarket</h2>
                <p className="w3-bar-item w3-left w3-white">Token {token}</p>
                <a className="w3-bar-item w3-button w3-right" onClick={logout}><h2>Log Out</h2></a>
                <a href="/create" className="w3-bar-item w3-button w3-right"><h2>Create Listing</h2></a>
                <a href="/home" className="w3-bar-item w3-button w3-right"><h2>Home</h2></a>
                <div className="w3-bar-item w3-right w3-margin">
                    <SearchBox />
                </div>
            </div>
        </div>
    )
}

export default Toolbar
