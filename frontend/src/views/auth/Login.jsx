import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { User, Lock, AlertCircle, Loader2, BookOpen } from 'lucide-react';
import bgImage from '../../assets/images/front1.jpeg'; 

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
            navigate('/dashboard');
        } else {
            setLocalError(result.message || 'Credenciales incorrectas');
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex font-sans bg-slate-50">
            
            {/* MITAD IZQUIERDA - IMAGEN */}
            <div className="hidden lg:flex lg:w-1/2 relative bg-slate-900">
                <img 
                    src={bgImage} 
                    alt="Campus Library" 
                    className="absolute inset-0 w-full h-full object-cover opacity-40"
                />
                <div className="relative z-10 w-full flex flex-col justify-center p-12 text-white">
                    <BookOpen className="h-16 w-16 text-red-500 mb-6" />
                    <h1 className="text-5xl font-bold mb-4 italic tracking-tighter">INFO CAMPUS</h1>
                    <p className="text-xl text-slate-200">
                        Tu portal académico integral. Gestiona tu futuro desde un solo lugar.
                    </p>
                </div>
            </div>

            {/* MITAD DERECHA - FORMULARIO */}
            <div className="flex-1 flex items-center justify-center p-8">
                <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-[40px] shadow-2xl border border-slate-100">
                    
                    <div className="text-center lg:text-left mb-8">
                        <h2 className="text-4xl font-black text-slate-900 tracking-tighter uppercase italic">
                            Iniciar Sesión
                        </h2>
                        <p className="mt-2 text-sm text-slate-500 font-medium">
                             Ingresa tus credenciales institucionales
                        </p>
                    </div>

                    <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                        <div className="space-y-5">
                            <div>
                                <label className="text-slate-700 text-xs font-black uppercase tracking-widest mb-2 block">Usuario</label>
                                <div className="relative flex items-center">
                                    <User className="w-5 h-5 absolute left-4 text-slate-400" />
                                    <input
                                        type="text"
                                        required
                                        className="w-full text-sm border border-slate-200 focus:border-red-500 focus:ring-4 focus:ring-red-50 rounded-2xl pl-12 pr-4 py-4 outline-none transition-all bg-slate-50/50"
                                        placeholder="Ej. a.romero"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="text-slate-700 text-xs font-black uppercase tracking-widest mb-2 block">Contraseña</label>
                                <div className="relative flex items-center">
                                    <Lock className="w-5 h-5 absolute left-4 text-slate-400" />
                                    <input
                                        type="password"
                                        required
                                        className="w-full text-sm border border-slate-200 focus:border-red-500 focus:ring-4 focus:ring-red-50 rounded-2xl pl-12 pr-4 py-4 outline-none transition-all bg-slate-50/50"
                                        placeholder="••••••••"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>

                        {localError && (
                            <div className="flex items-center gap-2 bg-red-50 border border-red-100 text-red-700 text-xs p-4 rounded-2xl animate-bounce">
                                <AlertCircle className="h-4 w-4 flex-shrink-0" />
                                <span className="font-bold">{localError}</span>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className={`
                                w-full flex justify-center items-center py-5 px-4 border border-transparent rounded-2xl shadow-xl text-sm font-black text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all active:scale-95
                                ${loading ? 'opacity-80 cursor-not-allowed' : ''}
                            `}
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="h-5 w-5 animate-spin mr-2" />
                                    AUTENTICANDO...
                                </>
                            ) : (
                                'ENTRAR AL PORTAL'
                            )}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;