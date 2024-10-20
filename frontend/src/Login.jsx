import React, { useState } from 'react';
import './Login.css';
import { login } from './authApi.js';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    console.log('Email:', email, 'Password:', password);
    console.log(login(email, password));
  };

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
          <button type="submit" className="login-button">LOGIN</button>
        </form>
        <p>
        Don’t have an account? <a href="/register">Create one here</a>
      </p>
        
      </div>
    </div>
  );
}

export default Login;
