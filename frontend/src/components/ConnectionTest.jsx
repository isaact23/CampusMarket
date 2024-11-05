// src/components/ConnectionTest.jsx
import { useState } from 'react'
import { api } from '../services/api'

function ConnectionTest() {
  const [getResponse, setGetResponse] = useState(null)
  const [postResponse, setPostResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const testGet = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.get('test/')
      setGetResponse(data)
    } catch (err) {
      setError(err.message)
    }
    setLoading(false)
  }

  const testPost = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.post('test/', {
        testData: 'Hello from React!',
        timestamp: new Date().toISOString()
      })
      setPostResponse(data)
    } catch (err) {
      setError(err.message)
    }
    setLoading(false)
  }

  return (
    <div>
      <h2>Connection Test</h2>
      <div>
        <button onClick={testGet} disabled={loading}>
          Test GET Request
        </button>
        <button onClick={testPost} disabled={loading}>
          Test POST Request
        </button>
      </div>
      
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      
      {getResponse && (
        <div>
          <h3>GET Response:</h3>
          <pre>{JSON.stringify(getResponse, null, 2)}</pre>
        </div>
      )}
      
      {postResponse && (
        <div>
          <h3>POST Response:</h3>
          <pre>{JSON.stringify(postResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default ConnectionTest