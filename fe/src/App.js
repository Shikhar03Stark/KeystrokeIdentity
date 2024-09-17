import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import KeyStrokeIntake from './components/KeyStrokeIntake';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Registration Page */}
          <Route path="/register" element={<RegistrationForm />} />
          
          {/* Next Steps after registration */}
          <Route path="/key-stroke-intake" element={<KeyStrokeIntake />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
