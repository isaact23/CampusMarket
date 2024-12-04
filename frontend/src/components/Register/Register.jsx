import React, { useState, useContext } from 'react';
import './Register.css';
import { register } from '../../services/authApi.js';
import { TokenContext } from "../../contexts/TokenContext.jsx"
import { useNavigate } from 'react-router-dom'
import LoadingIcon from '../LoadingIcon.jsx'

function Register() {
  const {token, setToken} = useContext(TokenContext)

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [isWaiting, setIsWaiting] = useState(false);

  const [showError, setShowError] = useState(false)
  const [errorText, setErrorText] = useState('')

  const navigate = useNavigate()

  const handleRegister = (e) => {
    e.preventDefault();

    setIsWaiting(true)
    register(username, email, password, (token) => {
      setToken(token)
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
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <label htmlFor="email">Student Email:</label>
          <input
            type="email"
            id="email"
            placeholder="Type your school email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            placeholder="Type your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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