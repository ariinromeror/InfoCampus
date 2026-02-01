import api from './api';

export const academicoService = {
    // 1. Obtiene inscripciones y notas (Usa la ruta automática del router)
    getMisInscripciones: () => api.get('inscripciones/'),
    
    // 2. Dashboards de gestión
    getStatsProfesor: () => api.get('profesor/dashboard/'),
    getStatsFinanzas: () => api.get('finanzas/dashboard/'),
    
    // 3. Descarga de PDF (Debe coincidir con path('finanzas/estado-cuenta/', ...))
    // EL responseType es OBLIGATORIO para que funcione
    descargarPDF: () => api.get('finanzas/estado-cuenta/', { 
        responseType: 'blob' 
    })
};