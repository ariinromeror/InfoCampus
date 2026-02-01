import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import { 
  DollarSign, 
  TrendingUp, 
  AlertTriangle,
  Users,
  CheckCircle,
  Loader2
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import StatCard from '../../components/cards/StatCard.jsx';

const TesoreroDashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    ingresoProyectado: 0,
    ingresoReal: 0,
    tasaCobranza: 0,
    estudiantesEnMora: 0
  });

  const API_URL = "http://127.0.0.1:8000/api/";

  useEffect(() => {
    fetchDatos();
  }, [user]);

  const fetchDatos = async () => {
    try {
      // Aquí conectarías con tu endpoint de tesorería
      // Por ahora, datos de ejemplo
      setStats({
        ingresoProyectado: 125000,
        ingresoReal: 98500,
        tasaCobranza: 78.8,
        estudiantesEnMora: 12
      });

      setLoading(false);
    } catch (err) {
      console.error("Error:", err);
      setLoading(false);
    }
  };

  // Datos para gráfico de pastel
  const pieData = [
    { name: 'Pagado', value: stats.ingresoReal, color: '#10b981' },
    { name: 'Pendiente', value: stats.ingresoProyectado - stats.ingresoReal, color: '#ef4444' }
  ];

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <Loader2 className="animate-spin text-red-600" size={48} />
        <p className="text-slate-400 font-bold">Cargando panel de tesorería...</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8"
    >
      {/* BIENVENIDA */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-8 rounded-3xl shadow-lg text-white">
        <h1 className="text-3xl font-black mb-2">
          Panel de Tesorería
        </h1>
        <p className="text-green-100">
          Gestión financiera y cobranza del período actual
        </p>
      </div>

      {/* ESTADÍSTICAS FINANCIERAS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Ingreso Proyectado"
          value={`$${stats.ingresoProyectado.toLocaleString()}`}
          icon={DollarSign}
          color="blue"
          subtitle="Total período"
        />

        <StatCard
          title="Ingreso Real"
          value={`$${stats.ingresoReal.toLocaleString()}`}
          icon={CheckCircle}
          color="green"
          subtitle="Cobrado a la fecha"
        />

        <StatCard
          title="Tasa de Cobranza"
          value={`${stats.tasaCobranza}%`}
          icon={TrendingUp}
          color="purple"
          subtitle="Meta: 85%"
        />

        <StatCard
          title="Estudiantes en Mora"
          value={stats.estudiantesEnMora}
          icon={AlertTriangle}
          color="red"
          subtitle="Requieren atención"
        />
      </div>

      {/* GRÁFICO DE COBRANZA */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100"
        >
          <h3 className="text-xl font-black text-slate-800 mb-6">
            📊 Estado de Cobranza
          </h3>
          
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            </PieChart>
          </ResponsiveContainer>

          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="text-center">
              <p className="text-2xl font-black text-green-600">
                ${stats.ingresoReal.toLocaleString()}
              </p>
              <p className="text-xs font-bold text-slate-500 uppercase">Cobrado</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-black text-red-600">
                ${(stats.ingresoProyectado - stats.ingresoReal).toLocaleString()}
              </p>
              <p className="text-xs font-bold text-slate-500 uppercase">Por Cobrar</p>
            </div>
          </div>
        </motion.div>

        {/* LISTA DE MOROSOS */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100"
        >
          <h3 className="text-xl font-black text-slate-800 mb-6">
            ⚠️ Estudiantes en Mora
          </h3>

          <div className="space-y-3">
            {[
              { nombre: 'Juan Pérez', deuda: 450, dias: 15 },
              { nombre: 'María García', deuda: 780, dias: 8 },
              { nombre: 'Carlos Ruiz', deuda: 320, dias: 22 },
              { nombre: 'Ana López', deuda: 890, dias: 5 }
            ].map((estudiante, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-red-50 rounded-xl border border-red-100"
              >
                <div>
                  <p className="font-bold text-slate-800 text-sm">
                    {estudiante.nombre}
                  </p>
                  <p className="text-xs text-slate-500">
                    {estudiante.dias} días de mora
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-black text-red-600">
                    ${estudiante.deuda}
                  </p>
                  <button className="text-xs font-bold text-blue-600 hover:text-blue-700">
                    Ver detalles
                  </button>
                </div>
              </div>
            ))}
          </div>

          <button className="w-full mt-4 bg-red-600 text-white py-3 rounded-xl font-bold hover:bg-red-700 transition-all">
            Ver Lista Completa
          </button>
        </motion.div>
      </div>

      {/* ACCIONES RÁPIDAS */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h3 className="text-xl font-black text-slate-800 mb-6">
          ⚡ Acciones Rápidas
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all text-center group">
            <CheckCircle className="mx-auto mb-3 group-hover:scale-110 transition-transform" size={32} />
            <p className="font-bold">Validar Pagos</p>
          </button>

          <button className="bg-gradient-to-br from-green-600 to-green-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all text-center group">
            <DollarSign className="mx-auto mb-3 group-hover:scale-110 transition-transform" size={32} />
            <p className="font-bold">Generar Reporte</p>
          </button>

          <button className="bg-gradient-to-br from-purple-600 to-purple-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all text-center group">
            <Users className="mx-auto mb-3 group-hover:scale-110 transition-transform" size={32} />
            <p className="font-bold">Lista Morosos</p>
          </button>

          <button className="bg-gradient-to-br from-orange-600 to-orange-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all text-center group">
            <AlertTriangle className="mx-auto mb-3 group-hover:scale-110 transition-transform" size={32} />
            <p className="font-bold">Enviar Recordatorios</p>
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default TesoreroDashboard;