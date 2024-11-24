import './Home.css'
import {get_homepage} from "./authApi"
import { useState, useEffect } from "react"

function Home() {
    const [products, setProducts] = useState([])
    useEffect(() => {
        const fetchProducts = async () => {
            const data = await get_homepage()
            console.log(data)
            setProducts(data)
        }

        fetchProducts()
    }, [])

    var cards = []
    cards.push(
        <div className="home-card w3-panel w3-margin w3-card-4 w3-black">
            <h1>Dell Enterprise 2500</h1>
        </div>
    )

    return (
        <div className="home">
            <div className="home-header w3-bar w3-card-4 w3-theme-d3 w3-top">
                <h2 className="w3-bar-item w3-left">CampusMarket</h2>
                <a href="/home" className="w3-bar-item w3-button w3-right"><h2>Home</h2></a>
            </div>
            <div className="home-content">
                {products.map((product) => (
                    <div className="home-card w3-panel w3-margin w3-card-4 w3-black">
                        <h1>{product.name}</h1>
                        <p>{product.description}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Home
