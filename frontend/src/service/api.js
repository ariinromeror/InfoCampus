import axios from 'axios';

// Configuración base de Axios
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// ✅ INTERCEPTOR: Agrega automáticamente el token a TODAS las peticiones
api.interceptors.request.use(
    (config) => {
        const userData = localStorage.getItem('campus_user');
        
        if (userData) {
            const user = JSON.parse(userData);
            if (user.access) {
                // ✅ FORMATO CORRECTO: Token <key>
                config.headers.Authorization = `Token ${user.access}`;
            }
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// ✅ INTERCEPTOR: Maneja errores 401 (token expirado o inválido)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token inválido o expirado
            localStorage.removeItem('campus_user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;