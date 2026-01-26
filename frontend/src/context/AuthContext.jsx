import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Recuperar sesión persistente de forma segura
        const storedUser = localStorage.getItem('campus_user');
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (error) {
                console.error("Error al restaurar sesión:", error);
                localStorage.removeItem('campus_user');
            }
        }
        setLoading(false);
    }, []);

    // Función de Login: Guarda toda la info del "Golden Dataset"
    const login = (userData) => {
        const enhancedUser = {
            ...userData,
            loginTime: new Date().getTime()
        };
        setUser(enhancedUser);
        localStorage.setItem('campus_user', JSON.stringify(enhancedUser));
    };

    // Función de Logout: Limpieza total
    const logout = () => {
        setUser(null);
        localStorage.clear(); // Limpia todo para evitar rastro de roles previos
        window.location.href = '/'; 
    };

    // Helpers de Roles (Para simplificar los componentes visuales)
    const isAdmin = user?.rol === 'director' || user?.rol === 'coordinador';
    const isStudent = user?.rol === 'estudiante';
    const isBlocked = user?.en_mora === true; // Bloqueo automático por Mora

    return (
        <AuthContext.Provider value={{ 
            user, 
            login, 
            logout, 
            loading,
            isAdmin,
            isStudent,
            isBlocked
        }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

// Hook personalizado para usar el contexto en cualquier parte
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth debe usarse dentro de un AuthProvider");
    }
    return context;
};