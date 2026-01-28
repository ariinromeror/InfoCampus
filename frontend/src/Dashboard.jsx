import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // <--- IMPORTAMOS EL NAVEGADOR
import { useAuth } from './context/AuthContext';
import { 
  BookOpen, 
  CheckCircle2,
  Loader2,
  TrendingUp,
  AlertCircle,
  AlertTriangle,
  XCircle
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate(); // <--- ACTIVAMOS EL NAVEGADOR
  const [materias, setMaterias] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_URL = "http://127.0.0.1:8000/api/";

  useEffect(() => {
    const fetchDatos = async () => {
      try {
        const response = await fetch(`${API_URL}historial/`, {
          headers: {
            'Authorization': `Bearer ${user?.access}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          setMaterias(data.map(item => ({
            id: item.id,
            nombre: item.materia_nombre,
            profesor: item.profesor_nombre || "Por asignar", 
            progreso: item.nota_final ? parseFloat(item.nota_final) * 10 : 0,
            nota: item.nota_final
          })));
        }
      } catch (err) {
        console.error("Error:", err);
      } finally {
        setLoading(false);
      }
    };

    if (user) fetchDatos();
  }, [user]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
      <Loader2 className="animate-spin text-red-600" size={48} />
      <p className="text-slate-400 font-bold">Cargando tu panel...</p>
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      
      {/* AVISO DE MORA CON BOTÓN FUNCIONAL */}
      {user?.en_mora && (
        <div className="bg-red-50 border-l-4 border-red-600 p-6 rounded-r-xl shadow-sm flex items-start gap-4">
            <div className="bg-white p-2 rounded-full shadow-sm text-red-600">
                <AlertTriangle size={32} />
            </div>
            <div>
                <h3 className="text-lg font-black text-red-700 uppercase">Aviso de Tesorería</h3>
                <p className="text-red-600 font-medium">
                    Estimado {user.username}, tienes pagos pendientes. 
                </p>
            </div>
            {/* ✅ AHORA ESTE BOTÓN SÍ FUNCIONA */}
            <button 
                onClick={() => navigate('/estado-cuenta')}
                className="ml-auto bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-red-700 shadow-md"
            >
                VER DÓNDE PAGAR
            </button>
        </div>
      )}

      {/* TARJETAS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="bg-blue-50 p-3 rounded-2xl text-blue-600"><TrendingUp size={24}/></div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Promedio</p>
            <p className="text-2xl font-black text-slate-800">{user?.en_mora ? '--' : '8.5'}</p>
          </div>
        </div>

        <div className={`p-6 rounded-3xl shadow-sm border flex items-center gap-4 ${user?.en_mora ? 'bg-red-50 border-red-100' : 'bg-white border-slate-100'}`}>
          <div className={`p-3 rounded-2xl ${user?.en_mora ? 'bg-red-200 text-red-700' : 'bg-emerald-50 text-emerald-600'}`}>
            {user?.en_mora ? <XCircle size={24}/> : <CheckCircle2 size={24}/>}
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Estado Cuenta</p>
            <p className={`text-2xl font-black ${user?.en_mora ? 'text-red-600' : 'text-emerald-600'}`}>
                {user?.en_mora ? 'PENDIENTE' : 'AL DÍA'}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="bg-purple-50 p-3 rounded-2xl text-purple-600"><BookOpen size={24}/></div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase">Materias</p>
            <p className="text-2xl font-black text-slate-800">{materias.length}</p>
          </div>
        </div>
      </div>

      {/* MATERIAS */}
      <div>
        <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
          <AlertCircle className="text-slate-400" /> Rendimiento Académico
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {materias.length > 0 ? materias.map((m) => (
            <div key={m.id} className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
              <div className="flex justify-between items-start mb-4">
                <h4 className="font-bold text-slate-800 uppercase text-sm">{m.nombre}</h4>
                <span className="text-xs font-black text-blue-600">NOTA: {m.nota}</span>
              </div>
              <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden mb-4">
                <div className="h-full bg-blue-600 rounded-full" style={{ width: `${m.progreso}%` }}></div>
              </div>
              <p className="text-[10px] font-bold text-slate-400 uppercase">PROF. {m.profesor}</p>
            </div>
          )) : (
            <div className="col-span-full text-center py-12 bg-white rounded-3xl border-2 border-dashed border-slate-200">
              <p className="text-slate-400 font-bold italic text-sm">
                 {user?.en_mora 
                    ? "🔒 Información académica restringida por mora." 
                    : "No se encontraron materias."}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;