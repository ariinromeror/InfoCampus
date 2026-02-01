import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import { academicoService } from '../../services/academicoService'; 
import { 
  Users, BookOpen, ClipboardCheck, Loader2, 
  Edit3, Calendar, MapPin, ArrowRight, Bell,
  TrendingUp, Star, Layout
} from 'lucide-react';
import StatCard from '../../components/cards/StatCard.jsx';

const PageContainer = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, ease: [0.19, 1, 0.22, 1] }}
    className="space-y-10 pb-16"
  >
    {children}
  </motion.div>
);

const ProfesorDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [secciones, setSecciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    secciones: 0,
    estudiantes: 0,
    promedio: 0
  });

  useEffect(() => {
    fetchDatos();
  }, [user]);

  const fetchDatos = async () => {
    try {
      // Sincronización con el backend real (Fase 1.2)
      const response = await academicoService.getStatsProfesor();
      const data = response.data;
      
      setSecciones(data.mis_clases || []);
      setStats({
        secciones: data.total_secciones || 0,
        estudiantes: data.total_alumnos || 0,
        promedio: data.rendimiento_promedio || 0
      });
    } catch (err) {
      console.error("Error al cargar panel docente:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <Loader2 className="animate-spin text-indigo-600 mb-4" size={40} />
      <span className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-400">Preparando Aula Virtual</span>
    </div>
  );

  return (
    <PageContainer>
      {/* 1. HERO SECTION DARK (Coherente con Estudiante) */}
      <section className="relative overflow-hidden rounded-[40px] bg-slate-900 p-10 text-white shadow-2xl shadow-indigo-900/30">
        <div className="relative z-10 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
               <span className="px-3 py-1 bg-indigo-500/20 rounded-full text-[10px] font-black tracking-widest text-indigo-300 border border-indigo-500/30 uppercase">
                Panel Docente 2026
              </span>
            </div>
            <h1 className="text-5xl font-black italic tracking-tighter leading-none">
              BIENVENIDO, <span className="text-indigo-400 uppercase">{user?.first_name || user?.username}</span>
            </h1>
            <p className="text-slate-400 font-medium text-sm max-w-md">
              Gestiona tus {stats.secciones} secciones activas y supervisa el rendimiento de tus estudiantes.
            </p>
          </div>
          <div className="flex gap-4">
            <motion.button 
              whileHover={{ scale: 1.05 }} 
              className="bg-indigo-600 px-8 py-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-xl shadow-indigo-500/20 flex items-center gap-3"
            >
              <Layout size={16} /> Reporte Global
            </motion.button>
          </div>
        </div>
        <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl"></div>
      </section>

      {/* 2. MÉTRICAS DOCENTES */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="Secciones" value={stats.secciones} icon={BookOpen} color="indigo" subtitle="Bajo tu cargo" />
        <StatCard title="Alumnos" value={stats.estudiantes} icon={Users} color="blue" subtitle="Total inscritos" />
        <StatCard title="Rendimiento" value={`${stats.promedio}`} icon={TrendingUp} color="emerald" subtitle="Promedio grupal" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 3. MIS SECCIONES (Rediseño "Clean") */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between px-2">
            <div className="flex items-center gap-3">
              <div className="w-1.5 h-8 bg-indigo-600 rounded-full"></div>
              <h2 className="text-2xl font-black text-slate-900 uppercase italic tracking-tighter">Mis Secciones</h2>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {secciones.map((seccion, idx) => (
              <motion.div 
                key={seccion.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white p-8 rounded-[35px] border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-indigo-500/5 transition-all group relative overflow-hidden"
              >
                <div className="relative z-10 flex flex-col h-full">
                  <div className="flex justify-between items-start mb-6">
                    <div className="space-y-2">
                      <span className="text-[10px] font-black text-indigo-500 uppercase tracking-widest">Sección {seccion.codigo}</span>
                      <h4 className="text-xl font-black text-slate-900 uppercase italic leading-tight group-hover:text-indigo-600 transition-colors">
                        {seccion.materia}
                      </h4>
                    </div>
                    <div className="bg-slate-950 text-white w-12 h-12 rounded-2xl flex flex-col items-center justify-center">
                      <span className="text-sm font-black">{seccion.estudiantes}</span>
                      <span className="text-[6px] font-black uppercase">Alum</span>
                    </div>
                  </div>

                  <div className="space-y-3 mb-8">
                    <div className="flex items-center gap-3 text-slate-400 text-[10px] font-black uppercase tracking-widest">
                      <Calendar size={14} className="text-indigo-500" />
                      {seccion.horario}
                    </div>
                    <div className="flex items-center gap-3 text-slate-400 text-[10px] font-black uppercase tracking-widest">
                      <MapPin size={14} className="text-indigo-500" />
                      Aula: {seccion.aula}
                    </div>
                  </div>

                  <div className="flex gap-3 pt-6 border-t border-slate-50">
                    <button 
                      onClick={() => navigate(`/seccion/${seccion.id}`)}
                      className="flex-1 py-3 bg-slate-900 text-white rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-indigo-600 transition-colors flex items-center justify-center gap-2"
                    >
                      <Users size={12} /> Gestionar
                    </button>
                    <button className="flex-1 py-3 bg-slate-50 text-slate-900 rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-slate-100 transition-colors flex items-center justify-center gap-2">
                      <Edit3 size={12} /> Notas
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* 4. ACTION CENTER DOCENTE */}
        <div className="space-y-6">
          <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] ml-2 flex items-center gap-2">
            <Bell size={12} className="text-indigo-500" /> Centro de Acción
          </h3>
          
          <div className="bg-white p-8 rounded-[40px] border border-slate-100 shadow-sm space-y-6">
            <div className="space-y-4">
              <div className="p-4 bg-amber-50 rounded-2xl border border-amber-100">
                <p className="text-[10px] font-black text-amber-800 uppercase italic">Pendiente de cierre</p>
                <p className="text-xs text-amber-700 font-medium mt-1">Faltan 5 notas por ingresar en Cálculo I.</p>
              </div>
              
              <div className="p-4 bg-indigo-50 rounded-2xl border border-indigo-100">
                <p className="text-[10px] font-black text-indigo-800 uppercase italic">Aviso Académico</p>
                <p className="text-xs text-indigo-700 font-medium mt-1">La carga de actas finaliza en 3 días.</p>
              </div>
            </div>

            <button className="w-full py-4 bg-slate-900 text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-slate-800 transition-all flex items-center justify-center gap-3">
              <Star size={16} className="text-amber-400" /> Ver Alumnos Destacados
            </button>
          </div>
        </div>
      </div>
    </PageContainer>
  );
};

export default ProfesorDashboard;