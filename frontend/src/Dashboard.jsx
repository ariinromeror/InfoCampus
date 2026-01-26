import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, 
  BookOpen, 
  QrCode, 
  LogOut, 
  User, 
  AlertCircle,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [materias, setMaterias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('inicio');
  const [qrToken, setQrToken] = useState(null);

  // URL base apuntando a tu servidor Django
  const API_URL = "http://127.0.0.1:8000/api/";

  useEffect(() => {
    const fetchDatosCompletos = async () => {
      // Si el usuario no existe o está en mora, detenemos la carga si es estudiante
      if (!user || (user.rol === 'estudiante' && user.en_mora)) {
        setLoading(false);
        return;
      }

      try {
        // Petición al endpoint que ya verificamos en el navegador
        const res = await axios.get(`${API_URL}mis-materias/`);
        
        const transformadas = res.data.map(item => ({
          id: item.id,
          nombre: item.nombre,
          profesor: item.profesor_nombre || "Catedrático Asignado", 
          // nota_valor viene como 9.5, lo convertimos a porcentaje (95%)
          progreso: item.nota_valor ? parseFloat(item.nota_valor) * 10 : 0
        }));
        
        setMaterias(transformadas);
      } catch (err) {
        console.error("Error al sincronizar con el Backend:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDatosCompletos();
  }, [user]);

  // Lógica para el Profesor: QR Dinámico (Corregido a singular 'asistencia')
  const handleGenerarQR = async () => {
    try {
      const res = await axios.get(`${API_URL}asistencia/generar_qr/`);
      setQrToken(res.data.token_dinamico);
      setView('qr');
    } catch (err) {
      alert("Error de conexión con el servidor de asistencia");
    }
  };

  const getProgressColor = (percent) => {
    if (percent < 30) return 'bg-red';
    if (percent < 61) return 'bg-yellow'; // 60 es la nota mínima de aprobación
    return 'bg-green';
  };

  return (
    <div className="dashboard-container">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-logo">INFO<span>CAMPUS</span></div>
        <nav style={{ flex: 1 }}>
          <div 
            className={`nav-item ${view === 'inicio' ? 'active' : ''}`} 
            onClick={() => setView('inicio')}
          >
            <LayoutDashboard size={20} style={{ marginRight: '10px' }} />
            Inicio
          </div>
          <div 
            className={`nav-item ${view === 'materias' ? 'active' : ''}`} 
            onClick={() => setView('materias')}
          >
            <BookOpen size={20} style={{ marginRight: '10px' }} />
            Mis Materias
          </div>
          {user.rol === 'profesor' && (
            <div 
              className={`nav-item ${view === 'qr' ? 'active' : ''}`} 
              onClick={handleGenerarQR}
            >
              <QrCode size={20} style={{ marginRight: '10px' }} />
              Asistencia QR
            </div>
          )}
        </nav>
        <div className="nav-item logout" onClick={onLogout} style={{ marginTop: 'auto' }}>
          <LogOut size={20} style={{ marginRight: '10px' }} />
          Cerrar Sesión
        </div>
      </aside>

      {/* CONTENIDO */}
      <main className="main-content">
        <header className="header-top">
          <div className="header-info">
            <h2 style={{ margin: 0 }}>
              {view === 'inicio' && 'Panel Principal'}
              {view === 'materias' && 'Malla Curricular'}
              {view === 'qr' && 'Control de Asistencia'}
            </h2>
            <p style={{ color: '#666', margin: 0 }}>{user.carrera_nombre || 'Ingeniería de Sistemas'}</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <h4>{user.first_name} {user.last_name}</h4>
              <p style={{ fontSize: '12px', color: '#cc0000', fontWeight: 'bold' }}>{user.rol.toUpperCase()}</p>
            </div>
            <div className="user-avatar"><User size={24} /></div>
          </div>
        </header>

        <div className="content-body">
          {loading ? (
            <div className="loader-box">
              <Loader2 className="spinner" size={40} />
              <p>Sincronizando con el servidor...</p>
            </div>
          ) : (
            <>
              {user.en_mora && user.rol === 'estudiante' ? (
                <div className="mora-card">
                  <AlertCircle size={80} color="#cc0000" />
                  <h1>Acceso Restringido</h1>
                  <p>Regulariza tus pagos en Tesorería para ver tus notas.</p>
                  <button className="btn-tesoreria">Ir a Pagos</button>
                </div>
              ) : (
                <>
                  {view === 'inicio' && (
                    <div className="subjects-grid">
                      {materias.length > 0 ? materias.map((m) => (
                        <div key={m.id} className="subject-card">
                          <div className="card-header">
                            <h4>{m.nombre}</h4>
                            {m.progreso >= 60 && <CheckCircle2 size={18} color="#2ecc71" />}
                          </div>
                          <p className="prof-tag">Prof: {m.profesor}</p>
                          <div className="progress-container">
                            <div 
                              className={`progress-bar ${getProgressColor(m.progreso)}`} 
                              style={{ width: `${m.progreso}%` }}
                            ></div>
                          </div>
                          <div className="card-footer">
                            <span>{m.progreso}% de aprobación</span>
                            <strong>Nota: {m.progreso / 10}</strong>
                          </div>
                        </div>
                      )) : <p>No se encontraron materias registradas.</p>}
                    </div>
                  )}

                  {view === 'materias' && (
                    <div className="table-card">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>Materia</th>
                            <th>Profesor</th>
                            <th>Calificación</th>
                            <th>Resultado</th>
                          </tr>
                        </thead>
                        <tbody>
                          {materias.map((m) => (
                            <tr key={m.id}>
                              <td>{m.nombre}</td>
                              <td>{m.profesor}</td>
                              <td>{m.progreso / 10} / 10.0</td>
                              <td>
                                <span className={m.progreso >= 60 ? 'status-pass' : 'status-fail'}>
                                  {m.progreso >= 60 ? 'Aprobada' : 'Reprobada'}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}

                  {view === 'qr' && (
                    <div className="qr-panel">
                      <h3>Código QR de Asistencia</h3>
                      <div className="qr-display">
                        {qrToken ? <QRCodeSVG value={qrToken} size={250} /> : <Loader2 className="spinner" />}
                      </div>
                      <button className="btn-refresh" onClick={handleGenerarQR}>Refrescar QR</button>
                    </div>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </main>

      <style>{`
        .loader-box { text-align: center; padding: 100px; color: #cc0000; }
        .spinner { animation: rotate 1s linear infinite; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .mora-card { text-align: center; padding: 80px; background: white; border-radius: 20px; }
        .btn-tesoreria { margin-top: 20px; background: #cc0000; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; }
        .prof-tag { font-size: 13px; color: #666; margin: 5px 0 15px 0; }
        .card-footer { display: flex; justify-content: space-between; font-size: 11px; margin-top: 10px; }
        .table-card { background: white; padding: 20px; border-radius: 15px; overflow-x: auto; }
        .data-table { width: 100%; border-collapse: collapse; }
        .data-table th, .data-table td { padding: 15px; border-bottom: 1px solid #eee; text-align: left; }
        .status-pass { color: #2e7d32; font-weight: bold; background: #e8f5e9; padding: 4px 8px; border-radius: 5px; }
        .status-fail { color: #d32f2f; font-weight: bold; background: #ffebee; padding: 4px 8px; border-radius: 5px; }
        .qr-panel { text-align: center; background: white; padding: 40px; border-radius: 20px; }
        .qr-display { margin: 30px auto; padding: 20px; width: fit-content; border: 15px solid #f9f9f9; border-radius: 15px; }
        .btn-refresh { background: #1a1a1a; color: white; border: none; padding: 10px 30px; border-radius: 10px; cursor: pointer; }
      `}</style>
    </div>
  );
};

export default Dashboard;