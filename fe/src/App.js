import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupForm from './components/SignupForm';
import KeyStrokeIntake from './components/KeyStrokeIntake';
import HomePage from './components/HomePage'; // Import the HomePage component
import './App.css'; // Import the CSS

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Home Page */}
          <Route path="/" element={<HomePage />} />
          
          {/* Registration Page */}
          <Route path="/signup" element={<SignupForm />} />
          
          {/* Next Steps after registration */}
          <Route path="/key-stroke-intake" element={<KeyStrokeIntake />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
