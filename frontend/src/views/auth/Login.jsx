import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LogIn, User, Lock, AlertCircle, Loader2 } from 'lucide-react';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [localError, setLocalError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setLocalError('');

        const result = await login(username, password);

        if (result.success) {
            // Obtenemos el usuario recién guardado para decidir la ruta
            const storedUser = JSON.parse(localStorage.getItem('campus_user'));
            
            // LÓGICA CAMALEÓN DE REDIRECCIÓN
            if (storedUser.en_mora && storedUser.rol === 'estudiante') {
                navigate('/blocked');
            } else if (['director', 'tesorero', 'coordinador', 'profesor'].includes(storedUser.rol)) {
                // Roles administrativos y docentes van al dashboard principal
                navigate('/dashboard');
            } else {
                navigate('/dashboard');
            }
        } else {
            setLocalError(result.message || 'Error al iniciar sesión');
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4 font-sans">
            <div className="max-w-md w-full space-y-8 bg-slate-800 p-10 rounded-2xl shadow-2xl border border-slate-700">
                <div className="text-center">
                    <div className="mx-auto h-12 w-12 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                        <LogIn className="text-white h-6 w-6" />
                    </div>
                    <h2 className="mt-6 text-3xl font-extrabold text-white tracking-tight text-center">
                        INFO CAMPUS
                    </h2>
                    <p className="mt-2 text-sm text-slate-400">
                        Inicia sesión para acceder a tu portal
                    </p>
                </div>
                
                <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
                    <div className="space-y-4">
                        <div>
                            <label className="text-slate-400 text-xs font-semibold uppercase">Usuario</label>
                            <div className="relative mt-1">
                                <User className="absolute left-3 top-3 h-5 w-5 text-slate-500" />
                                <input
                                    type="text"
                                    required
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-600 rounded-xl bg-slate-900 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                    placeholder="Tu username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>

                        <div>
                            <label className="text-slate-400 text-xs font-semibold uppercase">Contraseña</label>
                            <div className="relative mt-1">
                                <Lock className="absolute left-3 top-3 h-5 w-5 text-slate-500" />
                                <input
                                    type="password"
                                    required
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-600 rounded-xl bg-slate-900 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {localError && (
                        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/50 text-red-500 text-sm p-3 rounded-xl">
                            <AlertCircle className="h-4 w-4" />
                            <span>{localError}</span>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex justify-center items-center py-3 text-sm font-bold rounded-xl text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-lg"
                    >
                        {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : 'ENTRAR AL PORTAL'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;