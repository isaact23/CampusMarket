import './Home.css'
import Toolbar from "./Toolbar/Toolbar.jsx"
import Content from "./Content/Content.jsx"

function Home() {
    return (
        <div className="home">
            <Toolbar />
            <Content />
        </div>
    )
}

export default Home
