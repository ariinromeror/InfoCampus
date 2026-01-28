import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./views/auth/Login"; 
import Dashboard from "./Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import MainLayout from "./layouts/MainLayout.jsx";

function App() {
  return (
    <Router>
      <Routes>
        {/* 1. RUTA PÚBLICA: El Login no lleva Sidebar */}
        <Route path="/login" element={<Login />} />

        {/* 2. RUTAS PROTEGIDAS: Todas envueltas en el MainLayout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          {/* Todas estas rutas aparecerán dentro del <Outlet /> del MainLayout */}
          <Route path="dashboard" element={<Dashboard />} />
          
          {/* Aquí es donde agregaremos más adelante: 
              <Route path="notas" element={<Notas />} /> 
          */}
          
          {/* Redirección interna: si entras a "/" te manda a "/dashboard" */}
          <Route index element={<Navigate to="/dashboard" replace />} />
        </Route>

        {/* 3. REDIRECCIÓN GLOBAL: Si la ruta no existe, al dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;