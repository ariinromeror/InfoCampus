import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, 
  BookOpen, 
  QrCode, 
  LogOut, 
  User, 
  ShieldAlert,
  CheckCircle2,
  Loader2,
  CreditCard
} from 'lucide-react';

const Dashboard = ({ user, onLogout }) => {
  const [materias, setMaterias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('inicio');

  const API_URL = "http://127.0.0.1:8000/api/";

  useEffect(() => {
    const fetchDatos = async () => {
      try {
        const res = await axios.get(`${API_URL}mis-materias/`);
        setMaterias(res.data.map(item => ({
          id: item.id,
          nombre: item.nombre,
          profesor: item.profesor_nombre || "Catedrático Asignado", 
          progreso: item.nota_valor ? parseFloat(item.nota_valor) * 10 : 0
        })));
      } catch (err) {
        console.error("Error al cargar datos:", err);
      } finally {
        setLoading(false);
      }
    };

    // Lógica Camaleón: Si está en mora, no cargamos datos, solo mostramos el muro
    if (user && !(user.en_mora && user.rol === 'estudiante')) {
      fetchDatos();
    } else {
      setLoading(false);
    }
  }, [user]);

  const isMora = user?.en_mora && user?.rol === 'estudiante';

  return (
    <div className="flex min-h-screen bg-slate-50 font-sans">
      {/* SIDEBAR - Bloqueado si hay mora */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col p-6 transition-all border-r border-slate-800">
        <div className="text-2xl font-black tracking-tighter mb-10 text-blue-500">INFO<span className="text-white">CAMPUS</span></div>
        <nav className="flex-1 space-y-2">
          <div 
            onClick={() => !isMora && setView('inicio')} 
            className={`flex items-center gap-3 p-3 rounded-xl transition-all ${isMora ? 'opacity-20 cursor-not-allowed' : 'cursor-pointer hover:bg-slate-800'} ${view === 'inicio' && !isMora ? 'bg-blue-600 shadow-lg' : 'text-slate-400'}`}
          >
            <LayoutDashboard size={20} /> Inicio
          </div>
          <div 
            onClick={() => !isMora && setView('materias')} 
            className={`flex items-center gap-3 p-3 rounded-xl transition-all ${isMora ? 'opacity-20 cursor-not-allowed' : 'cursor-pointer hover:bg-slate-800'} ${view === 'materias' && !isMora ? 'bg-blue-600 shadow-lg' : 'text-slate-400'}`}
          >
            <BookOpen size={20} /> Mis Materias
          </div>
        </nav>
        
        <div onClick={onLogout} className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:bg-red-500/10 text-red-400 mt-auto transition-colors font-bold">
          <LogOut size={20} /> Cerrar Sesión
        </div>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="flex-1 flex flex-col overflow-hidden bg-white">
        <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-8">
          <div>
            <h2 className="text-xl font-bold text-slate-800">Portal Estudiantil</h2>
            <p className="text-[10px] text-slate-400 font-black tracking-[3px] uppercase">{user?.carrera_nombre || 'Informática'}</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <h4 className="text-sm font-bold text-slate-900 leading-tight">{user?.first_name} {user?.last_name}</h4>
              <span className={`text-[9px] px-2 py-0.5 rounded-full font-black tracking-tighter ${isMora ? 'bg-red-100 text-red-600' : 'bg-emerald-100 text-emerald-600'}`}>
                {isMora ? 'ACCESO RESTRINGIDO' : 'CUENTA ACTIVA'}
              </span>
            </div>
            <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500"><User size={20} /></div>
          </div>
        </header>

        <div className="p-8 flex-1 overflow-y-auto">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-full gap-4">
              <Loader2 className="animate-spin text-blue-600" size={40} />
              <p className="text-slate-400 font-bold text-sm">Sincronizando con Tesorería...</p>
            </div>
          ) : isMora ? (
            /* EL ANUNCIO CENTRAL (REEMPLAZA TODO EL CONTENIDO) */
            <div className="h-full flex items-center justify-center animate-in fade-in zoom-in duration-500">
              <div className="max-w-md w-full bg-white border border-slate-200 p-12 rounded-[40px] shadow-2xl text-center">
                <div className="w-24 h-24 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-8">
                  <ShieldAlert size={48} className="text-red-600" />
                </div>
                <h1 className="text-3xl font-black text-slate-900 mb-4 italic tracking-tighter">¡ALTO AHÍ!</h1>
                <p className="text-slate-500 mb-10 leading-relaxed text-sm">
                  Tu acceso académico ha sido suspendido temporalmente. Para visualizar tus notas y materias, debes ponerte al día con tus mensualidades.
                </p>
                <button 
                  onClick={() => window.location.href = 'https://pagos.infocampus.com'} 
                  className="w-full bg-red-600 text-white py-5 rounded-2xl font-black hover:bg-red-700 transition-all shadow-xl shadow-red-100 flex items-center justify-center gap-3 text-lg active:scale-95"
                >
                  <CreditCard size={24} /> IR A PAGAR AHORA
                </button>
                <p className="mt-8 text-[10px] text-slate-400 font-bold uppercase tracking-widest">Información: Departamento de Tesorería</p>
              </div>
            </div>
          ) : (
            /* CONTENIDO PARA ESTUDIANTES AL DÍA */
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {materias.length > 0 ? materias.map((m) => (
                <div key={m.id} className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-all">
                  <div className="flex justify-between items-start mb-4">
                    <h4 className="font-bold text-slate-800 leading-tight">{m.nombre}</h4>
                    {m.progreso >= 60 && <CheckCircle2 size={18} className="text-emerald-500" />}
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden mb-3">
                    <div className="h-full bg-blue-600 transition-all duration-1000" style={{ width: `${m.progreso}%` }}></div>
                  </div>
                  <div className="flex justify-between text-[10px] font-black text-slate-400">
                    <span>CUMPLIMIENTO</span>
                    <span className="text-blue-600">NOTA: {m.progreso / 10}</span>
                  </div>
                </div>
              )) : (
                <div className="col-span-full text-center py-20 bg-slate-50 rounded-3xl border-2 border-dashed border-slate-200">
                  <p className="text-slate-400 font-bold">No se encontraron materias cargadas en el sistema.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;