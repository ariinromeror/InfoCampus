import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, BookOpen, GraduationCap, LayoutDashboard, ClipboardList, User } from 'lucide-react';

const MainLayout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    return (
        <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
            
            {/* --- SIDEBAR IZQUIERDO (Estilo Institucional) --- */}
            <aside className="w-72 bg-white border-r border-slate-200 hidden md:flex flex-col shadow-sm">
                
                {/* Logo Institucional con Fondo Rojo */}
                <div className="h-20 flex items-center px-8 bg-red-700">
                    <BookOpen className="h-7 w-7 text-white mr-3" />
                    <span className="font-bold text-white text-lg tracking-tight">INFO CAMPUS</span>
                </div>

                {/* Navegación Principal */}
                <nav className="flex-1 px-4 py-8 space-y-1">
                    <p className="px-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">
                        Panel de Control
                    </p>
                    
                    <button 
                        onClick={() => navigate('/dashboard')}
                        className="w-full flex items-center px-4 py-3 text-sm font-semibold text-slate-600 hover:bg-red-50 hover:text-red-700 rounded-xl transition-all group"
                    >
                        <LayoutDashboard className="mr-3 h-5 w-5 text-slate-400 group-hover:text-red-700" />
                        Dashboard
                    </button>

                    {/* Links Dinámicos según Rol (RBAC) */}
                    {user?.rol === 'estudiante' && (
                        <>
                            <button className="w-full flex items-center px-4 py-3 text-sm font-semibold text-slate-600 hover:bg-red-50 hover:text-red-700 rounded-xl transition-all group">
                                <GraduationCap className="mr-3 h-5 w-5 text-slate-400 group-hover:text-red-700" />
                                Mis Notas
                            </button>
                            <button className="w-full flex items-center px-4 py-3 text-sm font-semibold text-slate-600 hover:bg-red-50 hover:text-red-700 rounded-xl transition-all group">
                                <ClipboardList className="mr-3 h-5 w-5 text-slate-400 group-hover:text-red-700" />
                                Horarios
                            </button>
                        </>
                    )}
                </nav>

                {/* Botón de Salir en el Sidebar */}
                <div className="p-6 border-t border-slate-100">
                    <button 
                        onClick={logout}
                        className="w-full flex items-center justify-center py-3 px-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-600 font-bold hover:bg-red-600 hover:text-white hover:border-red-600 transition-all text-xs"
                    >
                        <LogOut className="h-4 w-4 mr-2" />
                        CERRAR SESIÓN
                    </button>
                </div>
            </aside>

            {/* --- CONTENIDO PRINCIPAL --- */}
            <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
                
                {/* Header Superior (Blanco y Limpio) */}
                <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10">
                    
                    {/* Badge de Carrera / Info Izquierda */}
                    <div className="flex items-center space-x-3">
                        {user?.nombre_carrera && (
                            <span className="bg-red-50 text-red-700 px-3 py-1 rounded-full text-[11px] font-bold border border-red-100 uppercase">
                                {user.nombre_carrera}
                            </span>
                        )}
                        <span className="text-slate-300">|</span>
                        <h2 className="text-sm font-semibold text-slate-500 capitalize">
                            Portal {user?.rol}
                        </h2>
                    </div>

                    {/* Perfil del Usuario (Arriba Derecha) */}
                    <div className="flex items-center space-x-4">
                        <div className="text-right hidden sm:block">
                            <p className="text-sm font-bold text-slate-800 leading-none capitalize">
                                {user?.username}
                            </p>
                            <p className="text-[10px] font-bold text-red-600 uppercase mt-1 tracking-wider">
                                {user?.rol === 'estudiante' ? 'Alumno Regular' : user?.rol}
                            </p>
                        </div>
                        <div className="h-10 w-10 bg-red-700 rounded-full flex items-center justify-center text-white font-bold shadow-sm ring-4 ring-red-50">
                            {user?.username?.charAt(0).toUpperCase()}
                        </div>
                    </div>
                </header>

                {/* Espacio para las Vistas (Notas, Dashboard, etc) */}
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