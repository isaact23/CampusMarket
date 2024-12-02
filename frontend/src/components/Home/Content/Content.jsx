import './Content.css'

const Content = () => {
    /*const [products, setProducts] = useState([])
    useEffect(() => {
        const fetchProducts = async () => {
            const data = await get_homepage()
            console.log(data)
            setProducts(data)
        }

        fetchProducts()
    }, [])*/

    var cards = []
    cards.push(
        <div className="home-card w3-panel w3-margin w3-card-4 w3-black">
            <h1>Dell Enterprise 2500</h1>
        </div>
    )

    return (
        <div className="home-content">
            {cards}
        </div>
    )
}

export default Content


/*{products.map((product) => (
    <div className="home-card w3-panel w3-margin w3-card-4 w3-black">
        <h1>{product.name}</h1>
        <p>{product.description}</p>
    </div>
))}*/
