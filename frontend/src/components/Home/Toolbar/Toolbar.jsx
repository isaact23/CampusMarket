import SearchBox from "./SearchBox/SearchBox.jsx"

const Toolbar = () => {
    return (
        <div className="toolbar">
            <div className="home-header w3-bar w3-card-4 w3-theme-d3 w3-top">
                <h2 className="w3-bar-item w3-left">CampusMarket</h2>
                <a href="/login" className="w3-bar-item w3-button w3-right"><h2>Log Out</h2></a>
                <a href="/home" className="w3-bar-item w3-button w3-right"><h2>Home</h2></a>
                <div className="w3-bar-item w3-right w3-margin">
                    <SearchBox />
                </div>
            </div>
        </div>
    )
}

export default Toolbar
