import React from 'react';
import { Award, AlertCircle } from 'lucide-react';

const MisNotas = () => {
    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Título de la Habitación */}
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
                <div className="flex items-center gap-4 mb-4">
                    <div className="bg-red-50 p-4 rounded-2xl text-red-600">
                        <Award size={32} />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-slate-800">Boletín de Calificaciones</h1>
                        <p className="text-slate-500">Aquí verás tu progreso académico detallado.</p>
                    </div>
                </div>
                
                {/* Un aviso temporal hasta que conectemos los datos reales */}
                <div className="bg-blue-50 text-blue-800 p-4 rounded-xl flex items-center gap-3 text-sm font-bold mt-4">
                    <AlertCircle size={20} />
                    Esta es la vista de Notas (En construcción). Pronto verás tus datos aquí.
                </div>
            </div>
        </div>
    );
};

export default MisNotas;