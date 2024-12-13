import { useState, useEffect, useContext } from 'react'
import './Content.css'
import { AuthContext } from "../../../contexts/AuthContext.jsx"

const Content = () => {
  const { authApi } = useContext(AuthContext)

  const [listings, setListings] = useState([])
  const [loading, setLoading] = useState(true)

  const [showError, setShowError] = useState(false)
  const [errorText, setErrorText] = useState('')

  useEffect(() => {
    authApi.get('getHomepage/')
      .then(res => {
        let newListings = []
        res.products.forEach(product => {
          newListings.push({
            id: product.id,
            name: product.name,
            description: product.description,
            price: product.price,
            owner_id: product.owner_id
          })
          setListings(newListings)
        })
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setErrorText('An error occurred while fetching the homepage.')
        setShowError(true)
        setLoading(false)
      })
  }, [])

  const getErrorBox = () => {
    if (showError) {
      return (
        <div className="w3-panel w3-red w3-round-large">
          <h4 className="error-text">{errorText}</h4>
        </div>
      )
    }
    return ''
  }

  return (
    <div className="home-content">
      {loading ? <h1>Fetching products, please wait...</h1> : ''}
      {listings.map((product) => (
        <div className="home-card">
          <h1>{product.name}</h1>
          <p>{product.description}</p>
          <p>${product.price}</p>
        </div>
      ))}
      {getErrorBox()}
    </div>
  )
}

export default Content
