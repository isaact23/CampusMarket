import React, { useState, useContext } from 'react';
import './Register.css';
import { AuthContext } from "../../contexts/AuthContext.jsx"
import { useNavigate } from 'react-router-dom'
import LoadingIcon from '../LoadingIcon.jsx'

function Register() {
  const { authApi } = useContext(AuthContext)

  const [localUsername, setLocalUsername] = useState('');
  const [localEmail, setLocalEmail] = useState('');
  const [localPassword, setLocalPassword] = useState('');

  const [isWaiting, setIsWaiting] = useState(false);

  const [showError, setShowError] = useState(false)
  const [errorText, setErrorText] = useState('')

  const navigate = useNavigate()

  const handleRegister = (e) => {
    e.preventDefault();

    setIsWaiting(true)
    authApi.register(localUsername, localEmail, localPassword, (token) => {
      authApi.setEmail(localEmail)
      authApi.setToken(token)
      navigate('/home')
    }, (failMessage) => {
      setIsWaiting(false);
      setErrorText(failMessage)
      setShowError(true)
    })
  };

  const getButtonContents = () => {
    if (isWaiting) {
      return <LoadingIcon />
    } else {
      return "REGISTER"
    }
  }

  const getErrorBox = () => {
    if (showError) { return (
      <div className="w3-panel w3-red w3-round-large">
        <h4 className="error-text">{errorText}</h4>
      </div>
    )}
    return ''
  }

  return (
    <div className="register-container">
      <div className="register-box">
        <h2>Create Account</h2>
        <form onSubmit={handleRegister}>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            placeholder="Enter your username"
            value={localUsername}
            onChange={(e) => setLocalUsername(e.target.value)}
            required
          />
          <label htmlFor="email">Student Email:</label>
          <input
            type="email"
            id="email"
            placeholder="Type your school email"
            value={localEmail}
            onChange={(e) => setLocalEmail(e.target.value)}
            required
          />
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            placeholder="Type your password"
            value={localPassword}
            onChange={(e) => setLocalPassword(e.target.value)}
            required
          />
          <button type="submit" className="register-button">
            {getButtonContents()}
          </button>
          {getErrorBox()}
        </form>
        <p>
          Already have an account? <a href="/login">Log in here</a>
        </p>
      </div>
    </div>
  );
}

export default Register;