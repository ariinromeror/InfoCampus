import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
    LogOut, BookOpen, LayoutDashboard, 
    GraduationCap, ClipboardList, Wallet, AlertCircle,
    ChevronRight, Loader2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { academicoService } from '../services/academicoService';

const Sidebar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [secciones, setSecciones] = useState([]);
    const [loading, setLoading] = useState(false);

    // FASE 2.1: Carga dinámica de secciones para el Profesor
    useEffect(() => {
        if (user?.rol === 'profesor') {
            cargarDatosProfesor();
        }
    }, [user]);

    const cargarDatosProfesor = async () => {
        try {
            setLoading(true);
            const response = await academicoService.getStatsProfesor();
            setSecciones(response.data.mis_clases || []);
        } catch (err) {
            console.error("Error al cargar secciones en sidebar:", err);
        } finally {
            setLoading(false);
        }
    };

    const handleNavigation = (path, restricted = false) => {
        if (restricted && user?.en_mora) {
            navigate('/estado-cuenta');
            return;
        }
        navigate(path);
    };

    const NavItem = ({ path, icon: Icon, label, restricted, badge = null }) => {
        const isActive = location.pathname === path;
        return (
            <button
                onClick={() => handleNavigation(path, restricted)}
                className={`
                    w-full flex items-center px-4 py-3.5 mb-1 text-xs font-bold rounded-xl transition-all group relative
                    ${isActive 
                        ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-900/20' 
                        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                    }
                `}
            >
                <Icon className={`mr-3 h-5 w-5 ${isActive ? 'text-white' : 'text-slate-500 group-hover:text-white'}`} />
                <span className="tracking-wide uppercase flex-1 text-left">{label}</span>
                
                {badge}
                
                {restricted && user?.en_mora && (
                    <AlertCircle className="absolute right-4 h-4 w-4 text-amber-500 animate-pulse" />
                )}
            </button>
        );
    };

    return (
        <aside className="w-72 bg-slate-900 border-r border-slate-800 hidden md:flex flex-col shadow-2xl z-20">
            {/* LOGO INSTITUCIONAL */}
            <div className="h-24 flex flex-col justify-center px-8 border-b border-slate-800 bg-slate-950">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-indigo-600 rounded-lg">
                        <BookOpen className="h-5 w-5 text-white" />
                    </div>
                    <div>
                        <span className="font-black text-white text-lg tracking-tighter italic block leading-none">
                            INFO CAMPUS
                        </span>
                        <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase">
                            Portal Académico
                        </span>
                    </div>
                </div>
            </div>

            {/* MENÚ DINÁMICO POR ROL */}
            <nav className="flex-1 px-4 py-8 space-y-1 overflow-y-auto custom-scrollbar">
                <p className="px-4 text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4">General</p>
                <NavItem path="/dashboard" icon={LayoutDashboard} label="Dashboard" />

                {/* VISTA ESTUDIANTE */}
                {user?.rol === 'estudiante' && (
                    <>
                        <div className="my-6 border-t border-slate-800 mx-4"></div>
                        <p className="px-4 text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4">Académico</p>
                        <NavItem path="/notas" icon={GraduationCap} label="Mis Calificaciones" restricted />
                        <NavItem path="/horarios" icon={ClipboardList} label="Horario de Clases" restricted />
                        
                        <div className="my-6 border-t border-slate-800 mx-4"></div>
                        <p className="px-4 text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4">Financiero</p>
                        <NavItem 
                            path="/estado-cuenta" 
                            icon={Wallet} 
                            label="Tesorería y Pagos" 
                            badge={user?.en_mora && <span className="w-2 h-2 bg-red-500 rounded-full ml-2" />}
                        />
                    </>
                )}

                {/* VISTA PROFESOR: SECCIONES REALES */}
                {user?.rol === 'profesor' && (
                    <>
                        <div className="my-6 border-t border-slate-800 mx-4"></div>
                        <p className="px-4 text-[9px] font-black text-slate-600 uppercase tracking-[0.2em] mb-4 flex justify-between items-center">
                            Mis Secciones
                            {loading && <Loader2 className="animate-spin h-3 w-3" />}
                        </p>
                        {secciones.map((clase) => (
                            <button
                                key={clase.id}
                                onClick={() => navigate(`/seccion/${clase.id}`)}
                                className="w-full flex flex-col px-4 py-3 mb-2 rounded-xl border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-800/50 transition-all text-left group"
                            >
                                <span className="text-[10px] font-black text-indigo-400 uppercase truncate">
                                    {clase.materia}
                                </span>
                                <div className="flex justify-between items-center mt-1">
                                    <span className="text-[9px] text-slate-500 font-bold uppercase">{clase.codigo}</span>
                                    <ChevronRight className="h-3 w-3 text-slate-700 group-hover:text-indigo-400 transition-colors" />
                                </div>
                            </button>
                        ))}
                    </>
                )}
            </nav>

            {/* FOOTER - PERFIL Y CIERRE */}
            <div className="p-4 border-t border-slate-800 bg-slate-950/50">
                <div className="flex items-center gap-3 px-2 mb-4">
                    <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-[10px] font-black text-indigo-400 border border-slate-700 uppercase">
                        {user?.username?.substring(0, 2)}
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <p className="text-[10px] font-black text-white truncate uppercase italic">{user?.username}</p>
                        <p className="text-[8px] text-slate-500 font-bold uppercase tracking-widest">{user?.rol}</p>
                    </div>
                </div>
                <button 
                    onClick={logout} 
                    className="w-full flex items-center justify-center py-3 px-4 rounded-xl border border-slate-800 text-slate-400 font-bold hover:bg-red-500/10 hover:text-red-400 hover:border-red-500/50 transition-all text-xs group"
                >
                    <LogOut className="h-4 w-4 mr-2 group-hover:scale-110 transition-transform" /> 
                    CERRAR SESIÓN
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;