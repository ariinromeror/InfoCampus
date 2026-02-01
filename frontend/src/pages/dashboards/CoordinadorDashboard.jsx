import React from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import DirectorDashboard from './DirectorDashboard';

const CoordinadorDashboard = () => {
  const { user } = useAuth();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* Header específico del coordinador */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-8 rounded-3xl shadow-lg text-white mb-8">
        <h1 className="text-3xl font-black mb-2">
          Coordinación Académica
        </h1>
        <p className="text-purple-100">
          {user?.carrera_detalle?.nombre || 'Carrera'} | Gestión de Programa
        </p>
      </div>

      {/* Reutiliza componentes del director pero filtrados */}
      <DirectorDashboard />
    </motion.div>
  );
};

export default CoordinadorDashboard;