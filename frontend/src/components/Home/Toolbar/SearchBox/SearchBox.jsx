import React, { useState, useContext } from "react";
import "./SearchBox.css"
import { AuthContext } from "../../../../contexts/AuthContext.jsx"

const SearchBox = () => {
  const { authApi } = useContext(AuthContext)

  const [query, setQuery] = useState(""); // User input for the search query
  const [results, setResults] = useState([]); // Search results from the backend
  const [loading, setLoading] = useState(false); // Loading indicator
  const [error, setError] = useState(null); // Error state for API call failures

  // Function to handle the search
  const handleSearch = async () => {
    if (!query.trim()) {
      alert("Please enter a search term!"); // Prevent empty searches
      return;
    }

    setLoading(true); // Start the loading state
    setError(null); // Clear any previous errors

    try {
      // Make the API call using the `api.get` helper
      const response = await authApi.get(`search/?query=${encodeURIComponent(query)}`);
      setResults(response); // Update results with API response
    } catch (err) {
      setError(err.message || "An error occurred while fetching search results."); // Handle errors
    } finally {
      setLoading(false); // Stop the loading state
    }
  };

  return (
    <div className="searchbox-container">
      <input
        type="text"
        placeholder="Search for products..."
        value={query}
        onChange={(e) => setQuery(e.target.value)} // Update the query state on input change
        onKeyDown={(e) => e.key === "Enter" && handleSearch()} // Trigger search on Enter key
        className="searchbox-input"
      />
      <button onClick={handleSearch} className="searchbox-button">
        Search
      </button>

      {/* Display loading, error, or results */}
      {loading && <p>Loading...</p>}
      {error && <p className="error-message">{error}</p>}

      {results.length > 0 && (
        <ul className="search-results">
          {results.map((product) => (
            <li key={product.id} className="search-result-item">
              <h3>{product.name}</h3>
              <p>{product.description}</p>
              <p>Price: ${product.price}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBox;
