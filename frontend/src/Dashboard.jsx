import React, { useState, useEffect } from 'react';
import { useAuth } from './context/AuthContext';
import { 
  BookOpen, 
  ShieldAlert,
  CheckCircle2,
  Loader2,
  CreditCard,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [materias, setMaterias] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_URL = "http://127.0.0.1:8000/api/";

  useEffect(() => {
    const fetchDatos = async () => {
      try {
        // Usamos el endpoint que definimos en el backend
        const response = await fetch(`${API_URL}historial/`, {
          headers: {
            'Authorization': `Bearer ${user?.access}`,
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        
        if (response.ok) {
          setMaterias(data.map(item => ({
            id: item.id,
            nombre: item.materia_nombre,
            profesor: item.profesor_nombre || "Catedrático Asignado", 
            progreso: item.nota_final ? parseFloat(item.nota_final) * 10 : 0,
            nota: item.nota_final
          })));
        }
      } catch (err) {
        console.error("Error al cargar datos:", err);
      } finally {
        setLoading(false);
      }
    };

    if (user && !user.en_mora) {
      fetchDatos();
    } else {
      setLoading(false);
    }
  }, [user]);

  // Si está cargando, mostramos el spinner estético
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Loader2 className="animate-spin text-red-600" size={48} />
        <p className="text-slate-500 font-bold animate-pulse">Sincronizando con el servidor académico...</p>
      </div>
    );
  }

  // CASO A: BLOQUEO POR MORA
  if (user?.en_mora) {
    return (
      <div className="max-w-2xl mx-auto mt-10 animate-in fade-in zoom-in duration-500">
        <div className="bg-white border-2 border-red-100 p-12 rounded-[40px] shadow-2xl text-center">
          <div className="w-24 h-24 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-8 ring-8 ring-red-50/50">
            <ShieldAlert size={48} className="text-red-600" />
          </div>
          <h1 className="text-3xl font-black text-slate-900 mb-4 tracking-tighter uppercase">Acceso Restringido</h1>
          <p className="text-slate-500 mb-10 leading-relaxed">
            Estimado/a <strong>{user.username}</strong>, tu acceso al panel de calificaciones ha sido suspendido por pagos pendientes.
          </p>
          <button 
            onClick={() => window.open('https://pagos.infocampus.com', '_blank')} 
            className="w-full bg-red-600 text-white py-5 rounded-2xl font-black hover:bg-red-700 transition-all shadow-xl shadow-red-200 flex items-center justify-center gap-3 text-lg"
          >
            <CreditCard size={24} /> REGULARIZAR SITUACIÓN
          </button>
        </div>
      </div>
    );
  }

  // CASO B: DASHBOARD ACTIVO
  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      
      {/* 1. TARJETAS DE RESUMEN (Widgets rápidos) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="bg-red-50 p-3 rounded-2xl text-red-600"><TrendingUp size={24}/></div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Promedio General</p>
            <p className="text-2xl font-black text-slate-800">8.5</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="bg-red-50 p-3 rounded-2xl text-red-600"><BookOpen size={24}/></div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Materias Activas</p>
            <p className="text-2xl font-black text-slate-800">{materias.length}</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="bg-emerald-50 p-3 rounded-2xl text-emerald-600"><CheckCircle2 size={24}/></div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Estado Cuenta</p>
            <p className="text-2xl font-black text-emerald-600 italic">Al día</p>
          </div>
        </div>
      </div>

      {/* 2. LISTADO DE MATERIAS */}
      <div>
        <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
          <AlertCircle className="text-red-600" /> Rendimiento por Asignatura
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {materias.length > 0 ? materias.map((m) => (
            <div key={m.id} className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
              <div className="flex justify-between items-start mb-4">
                <h4 className="font-bold text-slate-800 leading-tight group-hover:text-red-700 transition-colors uppercase text-sm">{m.nombre}</h4>
                <div className="text-right">
                  <span className="text-xs font-black text-red-600">NOTA: {m.nota}</span>
                </div>
              </div>
              
              {/* Barra de Progreso Roja */}
              <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden mb-4">
                <div 
                  className="h-full bg-red-600 rounded-full transition-all duration-1000 ease-out" 
                  style={{ width: `${m.progreso}%` }}
                ></div>
              </div>
              
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-[10px] text-slate-500 font-bold">
                  {m.profesor.charAt(0)}
                </div>
                <span className="text-[10px] font-bold text-slate-400 uppercase">PROF. {m.profesor}</span>
              </div>
            </div>
          )) : (
            <div className="col-span-full text-center py-20 bg-white rounded-3xl border-2 border-dashed border-slate-200">
              <p className="text-slate-400 font-bold italic">No se encontraron registros académicos.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;