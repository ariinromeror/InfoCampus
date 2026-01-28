import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./views/auth/Login"; 
import Dashboard from "./Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import MainLayout from "./layouts/MainLayout.jsx";

import MisNotas from "./views/MisNotas";
import Horarios from "./views/Horarios";
import EstadoCuenta from "./views/EstadoCuenta"; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="notas" element={<MisNotas />} />
          <Route path="horarios" element={<Horarios />} />
          <Route path="estado-cuenta" element={<EstadoCuenta />} /> 
          
          <Route index element={<Navigate to="/dashboard" replace />} />
        </Route>

        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;