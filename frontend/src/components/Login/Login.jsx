import React, { useState, useContext } from 'react';
import './Login.css';
import { login } from '../../services/authApi.js';
import { TokenContext } from "../../contexts/TokenContext.jsx"
import { useNavigate } from 'react-router-dom'

function Login() {
  const {token, setToken} = useContext(TokenContext)

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  const [showError, setShowError] = useState(false)
  const [errorText, setErrorText] = useState('')

  const navigate = useNavigate()

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoggingIn(true);
    
    login(email, password, (token) => {
      setToken(token)
      navigate('/home')
    }, (failMessage) => {
      setIsLoggingIn(false);
      setErrorText(failMessage)
      setShowError(true)
    })
  };

  const getButtonContents = () => {
    if (isLoggingIn) {
      return <i className="fa fa-refresh w3-spin" />
    } else {
      return "LOGIN"
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
    <div className="login-container">
      <div className="login-box">
        <h2>Sign in</h2>
        <form onSubmit={handleLogin}>
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
          <div className="forgot-password">
            <a href="/forgot-password">Forgot password?</a>
          </div>
          <button type="submit" className="login-button" disabled={isLoggingIn}>
            {getButtonContents()}
          </button>
          {getErrorBox()}
        </form>
        <p>
          Don’t have an account? <a href="/register">Create one here</a>
        </p>
      </div>
    </div>
  );
}

export default Login;
