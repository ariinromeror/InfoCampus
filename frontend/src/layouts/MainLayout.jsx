import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const MainLayout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    return (
        <div className="flex h-screen bg-slate-900 text-white">
            {/* SIDEBAR PROVISIONAL (Lo haremos componente aparte luego) */}
            <aside className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
                <div className="p-6">
                    <h1 className="text-xl font-bold text-blue-500">INFO CAMPUS</h1>
                    <p className="text-xs text-slate-400 mt-1">v1.0 Pro</p>
                </div>

                <nav className="flex-1 px-4 space-y-2">
                    <div className="py-2 px-4 bg-blue-600/10 text-blue-400 rounded-lg font-medium">
                        🏠 Dashboard
                    </div>
                    {/* Aquí agregaremos links dinámicos según el rol después */}
                </nav>

                <div className="p-4 border-t border-slate-700">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-full bg-slate-600 flex items-center justify-center font-bold">
                            {user?.username?.charAt(0).toUpperCase()}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm font-medium truncate">{user?.first_name} {user?.last_name}</p>
                            <p className="text-xs text-slate-500 capitalize">{user?.rol}</p>
                        </div>
                    </div>
                    <button 
                        onClick={logout}
                        className="w-full py-2 px-4 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg text-sm font-medium transition-colors"
                    >
                        Cerrar Sesión
                    </button>
                </div>
            </aside>

            {/* CONTENIDO PRINCIPAL */}
            <main className="flex-1 flex flex-col overflow-hidden">
                <header className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-8">
                    <h2 className="font-semibold text-slate-300">
                        Bienvenido, {user?.rol === 'profesor' ? 'Prof.' : 'Estudiante'}
                    </h2>
                    <div className="flex items-center gap-4 text-sm text-slate-400">
                        <span>{new Date().toLocaleDateString()}</span>
                    </div>
                </header>

                <section className="flex-1 overflow-y-auto p-8">
                    {/* Outlet es donde se renderizarán los paneles (Estudiante o Profesor) */}
                    <Outlet />
                </section>
            </main>
        </div>
    );
};

export default MainLayout;