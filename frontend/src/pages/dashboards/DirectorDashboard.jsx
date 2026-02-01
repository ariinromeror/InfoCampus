import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import { 
  Users, 
  BookOpen, 
  DollarSign,
  TrendingUp,
  Award,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import StatCard from '../../components/cards/StatCard.jsx';

const DirectorDashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalEstudiantes: 0,
    totalProfesores: 0,
    ingresoMensual: 0,
    promedioInstitucional: 0,
    tasaRetencion: 0,
    alertasCriticas: 0
  });

  useEffect(() => {
    fetchDatos();
  }, [user]);

  const fetchDatos = async () => {
    try {
      // Datos de ejemplo - aquí conectarías con tu API
      setStats({
        totalEstudiantes: 450,
        totalProfesores: 45,
        ingresoMensual: 125000,
        promedioInstitucional: 8.3,
        tasaRetencion: 92,
        alertasCriticas: 3
      });

      setLoading(false);
    } catch (err) {
      console.error("Error:", err);
      setLoading(false);
    }
  };

  // Datos para gráfico de estudiantes por carrera
  const carrerasData = [
    { carrera: 'ING', estudiantes: 120 },
    { carrera: 'ADM', estudiantes: 95 },
    { carrera: 'MED', estudiantes: 80 },
    { carrera: 'DER', estudiantes: 85 },
    { carrera: 'PSI', estudiantes: 70 }
  ];

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <Loader2 className="animate-spin text-red-600" size={48} />
        <p className="text-slate-400 font-bold">Cargando panel ejecutivo...</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8"
    >
      {/* BIENVENIDA EJECUTIVA */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 p-8 rounded-3xl shadow-lg text-white">
        <h1 className="text-3xl font-black mb-2">
          Panel Ejecutivo - INFO CAMPUS
        </h1>
        <p className="text-slate-300">
          Director: {user?.first_name || user?.username} | Vista General del Sistema
        </p>
      </div>

      {/* ESTADÍSTICAS CLAVE */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard
          title="Estudiantes"
          value={stats.totalEstudiantes}
          icon={Users}
          color="blue"
        />

        <StatCard
          title="Profesores"
          value={stats.totalProfesores}
          icon={BookOpen}
          color="green"
        />

        <StatCard
          title="Ingreso Mensual"
          value={`$${(stats.ingresoMensual / 1000).toFixed(0)}K`}
          icon={DollarSign}
          color="purple"
        />

        <StatCard
          title="Promedio"
          value={stats.promedioInstitucional}
          icon={Award}
          color="orange"
        />

        <StatCard
          title="Retención"
          value={`${stats.tasaRetencion}%`}
          icon={TrendingUp}
          color="green"
        />

        <StatCard
          title="Alertas"
          value={stats.alertasCriticas}
          icon={AlertCircle}
          color="red"
        />
      </div>

      {/* GRÁFICOS Y ANÁLISIS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Estudiantes por Carrera */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100"
        >
          <h3 className="text-xl font-black text-slate-800 mb-6">
            📊 Estudiantes por Carrera
          </h3>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={carrerasData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis 
                dataKey="carrera" 
                stroke="#64748b"
                style={{ fontSize: '12px', fontWeight: 'bold' }}
              />
              <YAxis 
                stroke="#64748b"
                style={{ fontSize: '12px', fontWeight: 'bold' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: 'none',
                  borderRadius: '12px',
                  color: 'white',
                  fontWeight: 'bold'
                }}
              />
              <Bar dataKey="estudiantes" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Alertas Críticas */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100"
        >
          <h3 className="text-xl font-black text-slate-800 mb-6">
            ⚠️ Alertas del Sistema
          </h3>

          <div className="space-y-4">
            <div className="bg-red-50 border-l-4 border-red-600 p-4 rounded-r-xl">
              <div className="flex items-start gap-3">
                <AlertCircle className="text-red-600 mt-1" size={20} />
                <div>
                  <p className="font-black text-red-700 text-sm">
                    Mora Masiva - Ingeniería
                  </p>
                  <p className="text-xs text-red-600 mt-1">
                    15 estudiantes con más de 30 días de mora
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-orange-50 border-l-4 border-orange-600 p-4 rounded-r-xl">
              <div className="flex items-start gap-3">
                <AlertCircle className="text-orange-600 mt-1" size={20} />
                <div>
                  <p className="font-black text-orange-700 text-sm">
                    Cupos Limitados
                  </p>
                  <p className="text-xs text-orange-600 mt-1">
                    3 materias con cupos al 95% de capacidad
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 border-l-4 border-yellow-600 p-4 rounded-r-xl">
              <div className="flex items-start gap-3">
                <AlertCircle className="text-yellow-600 mt-1" size={20} />
                <div>
                  <p className="font-black text-yellow-700 text-sm">
                    Rendimiento Bajo - Cálculo II
                  </p>
                  <p className="text-xs text-yellow-600 mt-1">
                    Promedio de 5.8 - Requiere intervención
                  </p>
                </div>
              </div>
            </div>
          </div>

          <button className="w-full mt-4 bg-slate-800 text-white py-3 rounded-xl font-bold hover:bg-slate-900 transition-all">
            Ver Todas las Alertas
          </button>
        </motion.div>
      </div>

      {/* KPIs INSTITUCIONALES */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-3xl border border-blue-100"
      >
        <h3 className="text-xl font-black text-slate-800 mb-6">
          📈 Indicadores Clave de Rendimiento (KPIs)
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <p className="text-4xl font-black text-blue-600">92%</p>
            <p className="text-xs font-bold text-slate-600 uppercase mt-2">Tasa de Retención</p>
            <p className="text-xs text-green-600 font-bold mt-1">↑ 3% vs año anterior</p>
          </div>

          <div className="text-center">
            <p className="text-4xl font-black text-green-600">78%</p>
            <p className="text-xs font-bold text-slate-600 uppercase mt-2">Tasa de Cobranza</p>
            <p className="text-xs text-green-600 font-bold mt-1">Meta: 85%</p>
          </div>

          <div className="text-center">
            <p className="text-4xl font-black text-purple-600">8.3</p>
            <p className="text-xs font-bold text-slate-600 uppercase mt-2">Promedio Institucional</p>
            <p className="text-xs text-green-600 font-bold mt-1">↑ 0.2 puntos</p>
          </div>

          <div className="text-center">
            <p className="text-4xl font-black text-orange-600">94%</p>
            <p className="text-xs font-bold text-slate-600 uppercase mt-2">Satisfacción Estudiantil</p>
            <p className="text-xs text-green-600 font-bold mt-1">Encuesta semestral</p>
          </div>
        </div>
      </motion.div>

      {/* ACCESO RÁPIDO ADMINISTRATIVO */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h3 className="text-xl font-black text-slate-800 mb-6">
          ⚡ Gestión Rápida
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <button className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-all text-center group">
            <Users className="mx-auto mb-3 text-blue-600 group-hover:scale-110 transition-transform" size={32} />
            <p className="text-sm font-bold text-slate-700">Gestionar Usuarios</p>
          </button>

          <button className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-all text-center group">
            <BookOpen className="mx-auto mb-3 text-green-600 group-hover:scale-110 transition-transform" size={32} />
            <p className="text-sm font-bold text-slate-700">Malla Curricular</p>
          </button>

          <button className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-all text-center group">
            <DollarSign className="mx-auto mb-3 text-purple-600 group-hover:scale-110 transition-transform" size={32} />
            <p className="text-sm font-bold text-slate-700">Reportes Financieros</p>
          </button>

          <button className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-all text-center group">
            <Award className="mx-auto mb-3 text-orange-600 group-hover:scale-110 transition-transform" size={32} />
            <p className="text-sm font-bold text-slate-700">Rendimiento Académico</p>
          </button>

          <button className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-all text-center group">
            <AlertCircle className="mx-auto mb-3 text-red-600 group-hover:scale-110 transition-transform" size={32} />
            <p className="text-sm font-bold text-slate-700">Alertas del Sistema</p>
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default DirectorDashboard;