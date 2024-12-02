// src/App.jsx
import { useState, useEffect } from 'react'
import { api } from '../services/api'
import ConnectionTest from './components/ConnectionTest'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.get('test/')
        setMessage(data.message)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Django + React Integration Test</h1>
      
      {/* Simple Message Display */}
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="text-red-500">Error: {error}</p>
      ) : (
        <p className="mb-4">Message from Django: {message}</p>
      )}

      {/* Full Connection Test Component */}
      <ConnectionTest />
    </div>
  )
}

export default App