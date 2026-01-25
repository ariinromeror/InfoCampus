import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Lock, User, School, Loader2 } from 'lucide-react'; // Importamos Loader2 para el spinner
import campusImg from './assets/campus.jpg'; 
import Dashboard from './Dashboard'; // Importamos el componente que creamos antes

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // Estado para el spinner
  const [userSession, setUserSession] = useState(null); // Para guardar quién entró

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true); // ¡Empieza la carga!

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login/', {
        username,
        password
      });
      
      // Simulamos un pequeño delay de 1.5s para que se aprecie el spinner profesional
      setTimeout(() => {
        setUserSession(response.data);
        setLoading(false);
      }, 1500);

    } catch (err) {
      setLoading(false);
      setError('Credenciales institucionales no válidas.');
    }
  };

  // Si ya hay una sesión, mostramos el Dashboard
  if (userSession) {
    return <Dashboard user={userSession} onLogout={() => setUserSession(null)} />;
  }

  return (
    <div style={styles.container}>
      <div style={{...styles.background, backgroundImage: `url(${campusImg})`}}></div>
      
      <div style={styles.loginCard}>
        {loading ? (
          // --- ESTO ES EL SPINNER ---
          <div style={styles.loadingContainer}>
            <Loader2 size={50} color="#cc0000" style={styles.spinner} />
            <p style={styles.loadingText}>Verificando Identidad...</p>
          </div>
        ) : (
          // --- FORMULARIO NORMAL ---
          <>
            <div style={styles.header}>
              <div style={styles.logoContainer}>
                <School size={48} color="#cc0000" strokeWidth={2.5} /> 
              </div>
              <h1 style={styles.titleText}>INFO<span style={styles.titleThin}>CAMPUS</span></h1>
              <div style={styles.divider}></div>
              <p style={styles.subtitle}>SISTEMA DE GESTIÓN ACADÉMICA</p>
            </div>

            <form onSubmit={handleLogin}>
              {error && <div style={styles.errorBox}>{error}</div>}
              
              <div style={styles.inputWrapper}>
                <label style={styles.label}>Usuario</label>
                <div style={styles.inputGroup}>
                  <User size={18} style={styles.icon} />
                  <input 
                    type="text" 
                    style={styles.input}
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div style={styles.inputWrapper}>
                <label style={styles.label}>Contraseña</label>
                <div style={styles.inputGroup}>
                  <Lock size={18} style={styles.icon} />
                  <input 
                    type="password" 
                    style={styles.input}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              <button type="submit" style={styles.button}>
                INICIAR SESIÓN SEGURA
              </button>
            </form>
          </>
        )}
        
        <div style={styles.footer}>
          <p>INFOCAMPUS © 2026 | ACCESO RESTRINGIDO</p>
        </div>
      </div>

      {/* Estilo para la animación del spinner */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

const styles = {
  container: { height: '100vh', width: '100vw', display: 'flex', alignItems: 'center', justifyContent: 'flex-start', paddingLeft: '80px' },
  background: { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundSize: 'cover', backgroundPosition: 'center', filter: 'brightness(0.7)', zIndex: -1 },
  loginCard: { backgroundColor: 'rgba(255, 255, 255, 0.98)', padding: '60px 45px', borderRadius: '2px', boxShadow: '20px 0 50px rgba(0,0,0,0.3)', width: '100%', maxWidth: '420px', borderTop: '8px solid #cc0000' },
  loadingContainer: { display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 0' },
  spinner: { animation: 'spin 1s linear infinite' },
  loadingText: { marginTop: '20px', fontSize: '14px', fontWeight: '700', color: '#4b5563', letterSpacing: '1px' },
  header: { textAlign: 'center', marginBottom: '40px' },
  logoContainer: { marginBottom: '15px' },
  titleText: { margin: '0', color: '#1a1a1a', fontSize: '32px', fontWeight: '900', letterSpacing: '2px' },
  titleThin: { fontWeight: '300', color: '#cc0000' },
  divider: { height: '3px', width: '40px', backgroundColor: '#cc0000', margin: '15px auto' },
  subtitle: { color: '#4b5563', fontSize: '11px', letterSpacing: '3px', fontWeight: '700' },
  inputWrapper: { marginBottom: '25px' },
  label: { display: 'block', fontSize: '11px', fontWeight: '700', color: '#374151', marginBottom: '8px', textTransform: 'uppercase' },
  inputGroup: { display: 'flex', alignItems: 'center', borderBottom: '2px solid #e5e7eb', padding: '8px 0' },
  icon: { color: '#9ca3af', marginRight: '15px' },
  input: { border: 'none', outline: 'none', width: '100%', fontSize: '16px', background: 'transparent' },
  button: { width: '100%', padding: '16px', backgroundColor: '#cc0000', color: 'white', border: 'none', fontSize: '13px', fontWeight: '800', cursor: 'pointer', letterSpacing: '1px' },
  errorBox: { backgroundColor: '#fef2f2', color: '#dc2626', padding: '12px', fontSize: '13px', marginBottom: '20px', borderLeft: '4px solid #dc2626' },
  footer: { marginTop: '40px', fontSize: '9px', color: '#9ca3af', textAlign: 'center', letterSpacing: '1px' }
};

export default App;