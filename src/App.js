import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
// import ChatBot from './components/ChatBot';
import ChatScreen from './components/ChatScreen';
import LandingPage from './components/LandingPage';
import CampusTour from './components/CampusTour';
import GpaEvaluator from './components/GpaEvaluator';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          
          <Route path="/chat" element={<ChatScreen />} />

          <Route path="/campus" element={<CampusTour />} />

          <Route path="/gpa" element={<GpaEvaluator />} />

        </Routes>
      </Router>
    </div>
  );
}

export default App;
