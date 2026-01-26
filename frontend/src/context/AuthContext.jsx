import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

// URL Base del Backend - Centralizada para facilitar cambios de servidor
const API_URL = "http://127.0.0.1:8000/api";

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('campus_user');
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (err) {
                localStorage.removeItem('campus_user');
            }
        }
        setLoading(false);
    }, []);

    // Función de Login conectada al Backend de Django
    const login = async (username, password) => {
        setError(null);
        try {
            const response = await fetch(`${API_URL}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // El backend debe devolver el objeto usuario con sus flags (rol, en_mora, etc.)
                const userData = {
                    ...data.user,
                    token: data.token, // Si usas Token Auth
                    loginTime: new Date().getTime()
                };
                setUser(userData);
                localStorage.setItem('campus_user', JSON.stringify(userData));
                return { success: true };
            } else {
                setError(data.error || "Credenciales inválidas");
                return { success: false, message: data.error };
            }
        } catch (err) {
            setError("Error de conexión con el servidor");
            return { success: false, message: "No se pudo conectar con el servidor" };
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.clear();
        window.location.href = '/login';
    };

    // Helpers de estado para UI
    const isAdmin = user?.rol === 'director' || user?.rol === 'coordinador';
    const isStudent = user?.rol === 'estudiante';
    const isBlocked = user?.en_mora === true;

    return (
        <AuthContext.Provider value={{ 
            user, 
            login, 
            logout, 
            loading, 
            error,
            isAdmin, 
            isStudent, 
            isBlocked 
        }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth debe usarse dentro de un AuthProvider");
    return context;
};