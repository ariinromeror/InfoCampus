import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Login from "./pages/auth/Login";
import ProtectedRoute from "./components/ProtectedRoute";
import MainLayout from "./layout/MainLayout";

// Dashboards por rol 
import EstudianteDashboard from "./pages/dashboards/EstudianteDashboard";
import ProfesorDashboard from "./pages/dashboards/ProfesorDashboard";
import TesoreroDashboard from "./pages/dashboards/TesoreroDashboard";
import DirectorDashboard from "./pages/dashboards/DirectorDashboard";
import CoordinadorDashboard from "./pages/dashboards/CoordinadorDashboard";

// Vistas específicas
import MisNotas from "./views/MisNotas";
import Horarios from "./views/Horarios";
import EstadoCuenta from "./views/EstadoCuenta";

// Componente para redirigir según el rol
const DashboardRouter = () => {
  const { user } = useAuth();

  // Redirige al dashboard correspondiente según el rol
  switch (user?.rol) {
    case 'estudiante':
      return <EstudianteDashboard />;
    case 'profesor':
      return <ProfesorDashboard />;
    case 'tesorero':
      return <TesoreroDashboard />;
    case 'director':
      return <DirectorDashboard />;
    case 'coordinador':
      return <CoordinadorDashboard />;
    case 'administrativo':
      return <DirectorDashboard />;
    default:
      return <Navigate to="/login" replace />;
  }
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta pública */}
        <Route path="/login" element={<Login />} />

        {/* Rutas protegidas */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          {/* Dashboard dinámico según rol */}
          <Route path="dashboard" element={<DashboardRouter />} />

          {/* Rutas específicas */}
          <Route path="notas" element={<MisNotas />} />
          <Route path="horarios" element={<Horarios />} />
          <Route path="estado-cuenta" element={<EstadoCuenta />} />

          {/* Redirige / a dashboard */}
          <Route index element={<Navigate to="/dashboard" replace />} />
        </Route>

        {/* Ruta catch-all */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;