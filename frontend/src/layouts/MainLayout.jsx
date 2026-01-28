import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, BookOpen, GraduationCap, LayoutDashboard, ClipboardList } from 'lucide-react';

const MainLayout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    // Lógica inteligente para los clics
    const handleNavigation = (path) => {
        // Si el usuario es estudiante y tiene mora...
        if (user?.en_mora && (path === '/notas' || path === '/horarios')) {
            alert("🚫 SECCIÓN BLOQUEADA: Debes regularizar tu estado de cuenta en Tesorería para acceder.");
            navigate('/estado-cuenta'); // Lo mandamos a pagar automáticamente
            return;
        }
        navigate(path);
    };

    const isActive = (path) => location.pathname.includes(path);

    const btnClass = (path) => `w-full flex items-center px-4 py-3 text-sm font-semibold rounded-xl transition-all group mb-1 ${
        isActive(path) 
        ? 'bg-red-50 text-red-700 shadow-sm' 
        : 'text-slate-600 hover:bg-slate-50 hover:text-red-700'
    }`;

    return (
        <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
            <aside className="w-72 bg-white border-r border-slate-200 hidden md:flex flex-col shadow-sm">
                <div className="h-20 flex items-center px-8 bg-red-700">
                    <BookOpen className="h-7 w-7 text-white mr-3" />
                    <span className="font-bold text-white text-lg tracking-tight">INFO CAMPUS</span>
                </div>

                <nav className="flex-1 px-4 py-8 space-y-1">
                    <p className="px-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Panel de Control</p>
                    
                    <button onClick={() => handleNavigation('/dashboard')} className={btnClass('dashboard')}>
                        <LayoutDashboard className="mr-3 h-5 w-5" /> Dashboard
                    </button>

                    {user?.rol === 'estudiante' && (
                        <>
                            <button onClick={() => handleNavigation('/notas')} className={btnClass('notas')}>
                                <GraduationCap className="mr-3 h-5 w-5" /> Mis Notas
                            </button>
                            
                            <button onClick={() => handleNavigation('/horarios')} className={btnClass('horarios')}>
                                <ClipboardList className="mr-3 h-5 w-5" /> Horarios
                            </button>
                        </>
                    )}
                </nav>

                <div className="p-6 border-t border-slate-100">
                    <button onClick={logout} className="w-full flex items-center justify-center py-3 px-4 rounded-xl bg-slate-50 text-slate-600 font-bold hover:bg-red-600 hover:text-white transition-all text-xs">
                        <LogOut className="h-4 w-4 mr-2" /> CERRAR SESIÓN
                    </button>
                </div>
            </aside>

            <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
                <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10">
                    <div className="flex items-center space-x-3">
                        {user?.nombre_carrera && (
                            <span className="bg-red-50 text-red-700 px-3 py-1 rounded-full text-[11px] font-bold border border-red-100 uppercase">
                                {user.nombre_carrera}
                            </span>
                        )}
                        <span className="text-slate-300">|</span>
                        <h2 className="text-sm font-semibold text-slate-500 capitalize">Portal {user?.rol}</h2>
                    </div>

                    <div className="flex items-center space-x-4">
                        <div className="text-right hidden sm:block">
                            <p className="text-sm font-bold text-slate-800 leading-none capitalize">{user?.username}</p>
                            <p className="text-[10px] font-bold text-red-600 uppercase mt-1 tracking-wider">{user?.rol}</p>
                        </div>
                        <div className="h-10 w-10 bg-red-700 rounded-full flex items-center justify-center text-white font-bold">
                            {user?.username?.charAt(0).toUpperCase()}
                        </div>
                    </div>
                </header>

                <section className="flex-1 overflow-y-auto p-8 bg-slate-50/50">
                    <div className="max-w-6xl mx-auto">
                        <Outlet />
                    </div>
                </section>
            </main>
        </div>
    );
};

export default MainLayout;