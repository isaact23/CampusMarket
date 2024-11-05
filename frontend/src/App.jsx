// src/App.jsx
import { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/endpoint/')
      .then(response => response.json())
      .then(data => {
        setMessage(data.message)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching data:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      <h1>Django + React Integration Test</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <p>Message from Django: {message}</p>
      )}
    </div>
  )
}

export default App