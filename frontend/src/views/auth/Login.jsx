import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LogIn, User, Lock, AlertCircle, Loader2 } from 'lucide-react'; // Iconos pro

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            // URL conectada a tu backend de Django (Punto 1.1)
            const response = await axios.post('http://localhost:8000/api/login/', {
                username,
                password
            });

            if (response.data) {
                login(response.data);
                
                // Lógica Camaleón: Redirección según rol
                if (response.data.rol === 'director' || response.data.rol === 'coordinador') {
                    navigate('/admin-dashboard');
                } else {
                    navigate('/dashboard');
                }
            }
        } catch (err) {
            const msg = err.response?.data?.error || 'Credenciales inválidas. Inténtalo de nuevo.';
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4 font-sans">
            <div className="max-w-md w-full space-y-8 bg-slate-800 p-10 rounded-2xl shadow-2xl border border-slate-700 transition-all duration-300 hover:border-blue-500/30">
                
                {/* Header con Icono */}
                <div className="text-center">
                    <div className="mx-auto h-12 w-12 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-900/20">
                        <LogIn className="text-white h-6 w-6" />
                    </div>
                    <h2 className="mt-6 text-3xl font-extrabold text-white tracking-tight">
                        INFO CAMPUS
                    </h2>
                    <p className="mt-2 text-sm text-slate-400">
                        Gestión Universitaria de Próxima Generación
                    </p>
                </div>
                
                <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
                    <div className="space-y-4">
                        {/* Input de Usuario */}
                        <div className="relative">
                            <label className="text-slate-400 text-xs font-semibold uppercase ml-1">Usuario</label>
                            <div className="relative mt-1">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <User className="h-5 w-5 text-slate-500" />
                                </div>
                                <input
                                    type="text"
                                    required
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-600 rounded-xl bg-slate-900/50 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    placeholder="Ej: admin_gral"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>

                        {/* Input de Contraseña */}
                        <div className="relative">
                            <label className="text-slate-400 text-xs font-semibold uppercase ml-1">Contraseña</label>
                            <div className="relative mt-1">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-slate-500" />
                                </div>
                                <input
                                    type="password"
                                    required
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-600 rounded-xl bg-slate-900/50 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Mensaje de Error Dinámico */}
                    {error && (
                        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/50 text-red-500 text-sm p-3 rounded-xl animate-shake">
                            <AlertCircle className="h-4 w-4" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Botón de Acción */}
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full flex justify-center items-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-blue-600 hover:bg-blue-700 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all shadow-lg shadow-blue-900/20 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                    >
                        {loading ? (
                            <Loader2 className="h-5 w-5 animate-spin" />
                        ) : (
                            'ENTRAR AL PORTAL'
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;