import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupForm from './components/SignupForm';
import KeyStrokeIntake from './components/KeyStrokeIntake';
import HomePage from './components/HomePage';
import LandingPage from './components/LandingPage'; // Import the HomePage component
import './App.css'; // Import the CSS
import LoginForm from './components/LoginForm';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Home Page */}
          <Route path="/" element={<LandingPage />} />
          
          {/* Registration Page */}
          <Route path="/signup" element={<SignupForm />} />

          {/* Registration Page */}
          <Route path="/login" element={<LoginForm />} />
          
          {/* Next Steps after registration */}
          <Route path="/key-stroke-intake" element={<KeyStrokeIntake />} />

          {/* Home  Page after authentication */}
          <Route path="/home" element={<HomePage/>}></Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
