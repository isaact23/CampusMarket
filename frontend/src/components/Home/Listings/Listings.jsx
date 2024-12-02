import React, { useState } from 'react';
//import './Listings.css'

const Listings = () => {
  // State to manage the list of items for sale
  const [listings, setListings] = useState([]);
  
  // State to manage input for new listings
  const [newItem, setNewItem] = useState('');
  const [newAvailability, setNewAvailability] = useState(true);

  // Handle adding a new listing
  function handleAddListing() {
    if (newItem.trim()) {
      setListings([
        ...listings,
        { id: Date.now(), name: newItem, available: newAvailability }
      ]);
      setNewItem('');
      setNewAvailability(true);
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
    <div>
      <h1>Items for Sale</h1>

      {/* Input to add new item */}
      <input
        type="text"
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        placeholder="Enter item name"
      />
      <label>
        Available:
        <input
          type="checkbox"
          checked={newAvailability}
          onChange={(e) => setNewAvailability(e.target.checked)}
        />
      </label>
      <button onClick={handleAddListing}>Add Listing</button>

      <ul>
        {/* Display list of items */}
        {listings.map((item) => (
          <li key={item.id}>
            <span>{item.name} - {item.available ? 'Available' : 'Not Available'}</span>
            <button onClick={() => handleToggleAvailability(item.id)}>
              Toggle Availability
            </button>
            <button onClick={() => handleRemoveListing(item.id)}>
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Listings;
