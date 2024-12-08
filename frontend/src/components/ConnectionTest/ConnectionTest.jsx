// frontend/src/components/ConnectionTest.jsx
import { useState } from 'react'
import './ConnectionTest.css';
import { AuthContext } from "../../contexts/AuthContext.jsx"
import { useContext } from 'react'

function ConnectionTest() {
  const api = useContext(AuthContext)

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
    <div className="test-container">
      <div className="test-box">
        <h2>API Connection Test</h2>
        <div className="button-container">
          <button
            onClick={testGet}
            disabled={loading}
            className="test-button"
          >
            Test GET Request
          </button>
          <button
            onClick={testPost}
            disabled={loading}
            className="test-button"
          >
            Test POST Request
          </button>
        </div>
       
        {loading && <p className="loading">Loading...</p>}
        {error && <p className="error">Error: {error}</p>}
       
        {getResponse && (
          <div className="response-container">
            <h3>GET Response:</h3>
            <pre className="response-data">
              {JSON.stringify(getResponse, null, 2)}
            </pre>
          </div>
        )}
       
        {postResponse && (
          <div className="response-container">
            <h3>POST Response:</h3>
            <pre className="response-data">
              {JSON.stringify(postResponse, null, 2)}
            </pre>
          </div>
        )}
       
        <p>
          <a href="/login" className="back-link">Back to Login</a>
        </p>
      </div>
    </div>
  );
}

export default ConnectionTest;