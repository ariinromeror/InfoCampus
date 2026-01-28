import React from 'react';
import { Calendar, Clock } from 'lucide-react';

const Horarios = () => {
    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
                <div className="flex items-center gap-4 mb-6">
                    <div className="bg-red-50 p-4 rounded-2xl text-red-600">
                        <Calendar size={32} />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-slate-800">Horario de Clases</h1>
                        <p className="text-slate-500">Ciclo 2026 - Semestre I</p>
                    </div>
                </div>

                {/* Una tabla de ejemplo visual (Estática por ahora) */}
                <div className="overflow-hidden rounded-xl border border-slate-200">
                    <table className="min-w-full divide-y divide-slate-200">
                        <thead className="bg-slate-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase">Día</th>
                                <th className="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase">Hora</th>
                                <th className="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase">Materia</th>
                                <th className="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase">Aula</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-slate-200">
                            <tr>
                                <td className="px-6 py-4 text-sm font-bold text-slate-800">Lunes</td>
                                <td className="px-6 py-4 text-sm text-slate-500 flex items-center gap-2"><Clock size={14}/> 08:00 - 10:00</td>
                                <td className="px-6 py-4 text-sm text-slate-800">Matemáticas I</td>
                                <td className="px-6 py-4 text-sm text-red-600 font-bold">A-101</td>
                            </tr>
                            <tr>
                                <td className="px-6 py-4 text-sm font-bold text-slate-800">Miércoles</td>
                                <td className="px-6 py-4 text-sm text-slate-500 flex items-center gap-2"><Clock size={14}/> 10:00 - 12:00</td>
                                <td className="px-6 py-4 text-sm text-slate-800">Programación Básica</td>
                                <td className="px-6 py-4 text-sm text-red-600 font-bold">Lab-3</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Horarios;