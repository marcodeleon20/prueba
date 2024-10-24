import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Cart from './components/Cart';
import PurchaseReport from './components/PurchaseReport';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/report" element={<PurchaseReport />} />
      
      </Routes>
    </Router>
  );
}

export default App;

