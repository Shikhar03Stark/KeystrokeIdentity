import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RegistrationForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Simulating API call
      const response = await fetch('http://localhost:8000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const userId = data.id;  // Assuming the response contains the user ID.

        // Navigate to the next step, passing the user ID as state
        navigate('/key-stroke-intake', { state: { userId } });
      } else {
        setError('Registration failed. Please try again.');
      }
    } catch (error) {
      setError('An error occurred during registration.');
    }
  };

  return (
    <div className="RegistrationForm">
      <h2>Register</h2>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default RegistrationForm;
