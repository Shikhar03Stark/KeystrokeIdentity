import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css'; // Import the CSS for styling

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="homepage-container">
      <div className="content">
        <h1>Welcome to Our App Keystrokes Authentication</h1>
        <p className="intro-text">
          Discover a new way to authenticate yourself by tracking your keystrokes. We'll track your typing behaviour and identify if it's really you.
        </p>
        <div className="buttons-container">
          <button className="btn login-btn" onClick={() => navigate('/login')}>
            Login
          </button>
          <button className="btn signup-btn" onClick={() => navigate('/signup')}>
            Signup
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
