import React, { useState, useContext } from 'react';
import './Listings.css'
import LoadingIcon from '../../LoadingIcon.jsx'
import { AuthContext } from "../../../contexts/AuthContext.jsx"

const Listings = () => {
  const { authApi } = useContext(AuthContext)

  // State to manage the list of items for sale
  const [listings, setListings] = useState([]);
  
  // State to manage input for new listings
  const [newItem, setNewItem] = useState('');
  const [price, setPrice] = useState('');
  const [newAvailability, setNewAvailability] = useState(true);

  const [loading, setLoading] = useState(false)
  const [waiting, setWaiting] = useState(false)

  // Handle adding a new listing
  function handleAddListing() {
    if (newItem.trim()) {
      setWaiting(true)
      parseInt(price)

      authApi.postAuth('/addProduct', {
        name: newItem,
        description: '',
        price: price,
        available: newAvailability
      })
      .then(res => {
        setListings([
          ...listings,
          { id: Date.now(), name: newItem, available: newAvailability }
        ]);
        setNewItem('');
        setNewAvailability(true);
      })
    }
  }

  // Handle removing a listing
  const handleRemoveListing = (id) => {
    setListings(listings.filter(item => item.id !== id));
  };

  // Handle toggling the availability of an item
  const handleToggleAvailability = (id) => {
    setListings(
      listings.map(item =>
        item.id === id ? { ...item, available: !item.available } : item
      )
    );
  };

  return (
    <div className="listings">
      <div className="listings-box">
      <h1>Items for Sale</h1>

      <input
        type="text"
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        placeholder="Enter item name"
      />
      <div className="price-input">
        <input
          type="number"
          min="1"
          step="0.01"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          placeholder="1.00"
        />
      </div>
      <div className="listings-available">
        <label for="available-checkbox">Item is currently available:</label>
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
            <button className="toggle" onClick={() => handleToggleAvailability(item.id)}>
              Toggle Availability
            </button>
            <button  className="remove" onClick={() => handleRemoveListing(item.id)}>
              Remove
            </button>
          </li>
        ))}
      </ul>
      </div>
    </div>
  );
};

export default Listings;
