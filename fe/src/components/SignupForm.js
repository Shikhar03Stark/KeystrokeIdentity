import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignupForm.css'; // Import the new CSS for styling
import config from '../config'; // Import the config file

function RegistrationForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const backend_url = `http://${config.backend_host}` // http://keystroke.devitvish.in

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(`http://${backend_url}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const userId = data.id;

        navigate('/key-stroke-intake', { state: { userId } });
      } else {
        setError('Registration failed. Please try again.');
      }
    } catch (error) {
      setError('An error occurred during registration.');
    }
  };

  return (
    <div className="registration-container">
      <div className="registration-box">
        <h2>Create an Account</h2>
        {error && <p className="error-message">{error}</p>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Enter your username"
            />
          </div>
          
          <div className="input-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>
          
          <button type="submit" className="submit-btn">Register</button>
        </form>
      </div>
    </div>
  );
}

export default RegistrationForm;
