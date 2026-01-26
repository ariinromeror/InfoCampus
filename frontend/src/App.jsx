import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import BlockedScreen from './components/BlockedScreen';

function App() {
    return (
        <Router>
            <Routes>
                {/* --- RUTAS PÚBLICAS --- */}
                <Route path="/login" element={<Login />} />
                
                {/* --- RUTAS PROTEGIDAS (Fase 2.2: El Gatekeeper) --- */}
                <Route 
                    path="/dashboard" 
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    } 
                />

                {/* --- RUTA DE BLOQUEO ADMINISTRATIVO --- */}
                <Route path="/bloqueado" element={<BlockedScreen />} />

                {/* --- RUTAS FUTURAS (Fase 3: Paneles Administrativos) --- */}
                {/* Aquí añadiremos /admin-dashboard en el siguiente paso */}

                {/* --- REDIRECCIÓN AUTOMÁTICA --- */}
                {/* Si no está logueado, el ProtectedRoute lo mandará a /login */}
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;