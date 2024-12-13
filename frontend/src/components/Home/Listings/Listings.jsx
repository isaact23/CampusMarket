import React, { useState, useEffect, useContext } from 'react';
import './Listings.css'
import LoadingIcon from '../../LoadingIcon.jsx'
import { AuthContext } from "../../../contexts/AuthContext.jsx"

const Listings = () => {
  const { authApi } = useContext(AuthContext)

  // State to manage the list of items for sale
  const [listings, setListings] = useState([]);
  
  // State to manage input for new listings
  const [newItem, setNewItem] = useState('')
  const [newDescription, setNewDescription] = useState('')
  const [newPrice, setNewPrice] = useState('')
  const [newAvailability, setNewAvailability] = useState(true);

  const [loading, setLoading] = useState(true)
  const [waiting, setWaiting] = useState(false)

  const [errorText, setErrorText] = useState('')
  const [showError, setShowError] = useState(false)

  useEffect(() => {
    authApi.getAuth('/getProducts')
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
      setErrorText('An error occurred while fetching products.')
      setShowError(true)
      setLoading(false)
    })
  }, [])

  // Handle adding a new listing
  function handleAddListing() {
    if (newItem.trim() && newDescription.trim() && newPrice != '') {
      setWaiting(true)
      setShowError(false)

      authApi.postAuth('/addProduct/', {
        name: newItem,
        description: newDescription,
        price: newPrice,
        available: newAvailability
      })
      .then(res => {
        console.log(res.product_id)
        setListings([
          ...listings,
          { id: res.product_id,
            name: newItem,
            description: newDescription,
            price: newPrice,
            available: newAvailability }
        ]);
        setNewItem('');
        setNewAvailability(true);
        setWaiting(false)
      })
      .catch(err => {
        setWaiting(false)
        setErrorText("Something went wrong while adding the listing.")
        setShowError(true)
      })
    }
  }

  // Handle removing a listing
  const handleRemoveListing = (id) => {
    setWaiting(true)
    setShowError(false)

    authApi.postAuth('deleteProduct/', {
      id: id
    })
    .then(res => {
      setListings(listings.filter(item => item.id !== id))
      setWaiting(false)
    })
    .catch(err => {
      setWaiting(false)
      setErrorText("Something went wrong while removing the listing.")
      setShowError(true)
    })
  };

  // Handle toggling the availability of an item
  const handleToggleAvailability = (id) => {
    setListings(
      listings.map(item =>
        item.id === id ? { ...item, available: !item.available } : item
      )
    );
  };

  const getErrorBox = () => {
    if (showError) { return (
      <div className="w3-panel w3-red w3-round-large">
        <h4 className="error-text">{errorText}</h4>
      </div>
    )}
    return ''
  }

  const getListingsBox = () => {
    return (
      <div className="listings-box">
        <h1>Items for Sale</h1>

        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Enter item name"
        />
        <input
          type="text"
          value={newDescription}
          onChange={(e) => setNewDescription(e.target.value)}
          placeholder="Enter item description"
        />
        <div className="price-input">
          <input
            type="number"
            min="1"
            step="0.01"
            value={newPrice}
            onChange={(e) => setNewPrice(e.target.value)}
            placeholder="1.00"
          />
        </div>
        <div className="listings-available">
          <label for="available-checkbox">Is the item available?</label>
          <input
            type="checkbox"
            id="available-checkbox"  checked={newAvailability}
            onChange={(e) => setNewAvailability(e.target.checked)}
          />
        </div>
        <button onClick={handleAddListing} disabled={waiting}>
          {waiting ? <LoadingIcon /> : "Add Listing"}
        </button>

        <ul>
          {/* Display list of items */}
          {listings.map((item) => (
            <li key={item.id}>
              <span>{item.name} - {item.available ? 'Available' : 'Not Available'}</span>
              <span>{item.description.slice(0, 100)}</span>
              <span>${item.price}</span>
              <button className="toggle" onClick={() => handleToggleAvailability(item.id)}>
                Toggle Availability
              </button>
              <button className="remove" disabled={waiting} onClick={() => handleRemoveListing(item.id)}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      </div>
    )
  }

  return (
    <div className="listings">
      {loading ? <h1>Loading your listings...</h1> : getListingsBox()}
      {getErrorBox()}
    </div>
  );
};

export default Listings;
