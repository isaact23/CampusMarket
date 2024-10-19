import React, { useState } from 'react';
import './App.css'; // Use App.css for the styles

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // Add logic to handle login here
    console.log('Email:', email, 'Password:', password);
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
            <a href="#">Forgot password?</a>
          </div>
          <button type="submit" className="login-button">LOGIN</button>
        </form>
        <p>
        Don’t have an account? <a href="/create-account">Create one here</a>
      </p>
        
      </div>
    </div>
  );
}

export default App;


