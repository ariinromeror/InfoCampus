import React from 'react';
import { CreditCard, Landmark, AlertCircle, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const EstadoCuenta = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    return (
        <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in zoom-in duration-500">
            {/* Botón para volver */}
            <button 
                onClick={() => navigate('/dashboard')}
                className="flex items-center text-slate-500 hover:text-red-600 font-bold transition-colors gap-2"
            >
                <ArrowLeft size={20} /> VOLVER AL PANEL
            </button>

            <div className="bg-white rounded-[40px] shadow-xl overflow-hidden border border-slate-100">
                {/* Cabecera Azul/Institucional */}
                <div className="bg-slate-900 p-10 text-white">
                    <p className="text-slate-400 font-bold uppercase tracking-widest text-xs mb-2">Estado de Cuenta Académico</p>
                    <h1 className="text-3xl font-black">Detalle de Obligaciones</h1>
                </div>

                <div className="p-10 space-y-8">
                    {/* Resumen de Deuda */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-red-50 p-6 rounded-3xl border border-red-100">
                            <p className="text-red-600 font-bold text-sm uppercase">Total Pendiente</p>
                            <p className="text-4xl font-black text-red-700">$ 250.00</p>
                            <p className="text-red-500 text-xs mt-2 font-medium">* Corresponde a la cuota de Enero 2026</p>
                        </div>
                        <div className="bg-slate-50 p-6 rounded-3xl border border-slate-100 flex items-center gap-4">
                            <div className="bg-white p-3 rounded-2xl shadow-sm text-slate-600">
                                <AlertCircle size={24} />
                            </div>
                            <div>
                                <p className="text-slate-500 font-bold text-xs uppercase">Fecha Límite</p>
                                <p className="text-slate-800 font-black">05 de Febrero, 2026</p>
                            </div>
                        </div>
                    </div>

                    {/* Información Bancaria */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-black text-slate-800 flex items-center gap-2">
                            <Landmark className="text-red-600" size={20} /> Métodos de Pago Autorizados
                        </h3>
                        
                        <div className="grid grid-cols-1 gap-4">
                            <div className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-2xl hover:border-red-300 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="bg-slate-100 p-2 rounded-xl text-slate-700 font-bold text-xs">BANCO NACIONAL</div>
                                    <div>
                                        <p className="text-sm font-bold text-slate-800">Cuenta Corriente: 1902-3344-5566</p>
                                        <p className="text-xs text-slate-500">Info Campus S.A.</p>
                                    </div>
                                </div>
                                <button className="text-red-600 font-bold text-xs hover:underline">Copiar</button>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-2xl hover:border-red-300 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="bg-blue-100 p-2 rounded-xl text-blue-700 font-bold text-xs">PAGO ONLINE</div>
                                    <div>
                                        <p className="text-sm font-bold text-slate-800">Tarjeta de Crédito o Débito</p>
                                        <p className="text-xs text-slate-500">Procesamiento inmediato</p>
                                    </div>
                                </div>
                                <button className="bg-slate-900 text-white px-4 py-2 rounded-xl font-bold text-xs hover:bg-red-600 transition-colors">PAGAR AHORA</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EstadoCuenta;