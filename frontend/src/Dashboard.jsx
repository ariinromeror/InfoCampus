import React, { useState } from 'react';
import { 
  LayoutDashboard, BookOpen, GraduationCap, Settings, 
  LogOut, User as UserIcon, Bell, Calendar, ChevronRight 
} from 'lucide-react';

function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');

  const styles = {
    // Contenedor principal sin márgenes, ocupa el 100% real
    container: { 
      display: 'flex', 
      height: '100vh', 
      width: '100vw', 
      backgroundColor: '#f8fafc', 
      fontFamily: 'Inter, system-ui, sans-serif',
      overflow: 'hidden' 
    },
    // Sidebar fijo a la izquierda
    sidebar: { 
      width: '280px', 
      backgroundColor: '#0f172a', 
      color: 'white', 
      display: 'flex', 
      flexDirection: 'column',
      flexShrink: 0 
    },
    logoSection: { 
      padding: '25px', 
      fontSize: '24px', 
      fontWeight: 'bold', 
      borderBottom: '1px solid #1e293b',
      textAlign: 'left'
    },
    menu: { flex: 1, padding: '20px 0' },
    menuItem: (tab) => ({ 
      display: 'flex', alignItems: 'center', padding: '14px 25px', 
      color: activeTab === tab ? 'white' : '#94a3b8', 
      backgroundColor: activeTab === tab ? '#cc0000' : 'transparent',
      cursor: 'pointer', transition: 'all 0.2s ease',
      fontSize: '15px'
    }),
    // Área de la derecha que ocupa todo el resto
    mainWrapper: { 
      flex: 1, 
      display: 'flex', 
      flexDirection: 'column', 
      minWidth: 0 
    },
    // Header superior pegado a los bordes
    header: { 
      height: '70px',
      backgroundColor: 'white', 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      padding: '0 30px',
      borderBottom: '1px solid #e2e8f0',
      flexShrink: 0
    },
    // Contenedor de contenido + panel derecho
    bodyLayout: { 
      display: 'flex', 
      flex: 1, 
      overflow: 'hidden' 
    },
    contentScroll: { 
      flex: 1, 
      padding: '40px', 
      overflowY: 'auto' 
    },
    // Panel derecho estético
    rightPanel: { 
      width: '350px', 
      backgroundColor: 'white', 
      borderLeft: '1px solid #e2e8f0', 
      padding: '30px', 
      overflowY: 'auto',
      display: 'block' // Puedes usar 'none' en móviles si quisieras
    },
    userProfile: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '6px 12px',
      borderRadius: '50px',
      backgroundColor: '#f1f5f9',
      cursor: 'pointer'
    }
  };

  const RenderContent = () => {
    switch(activeTab) {
      case 'cursos': return (
        <div>
          <h1 style={{fontSize: '32px', marginBottom: '10px'}}>📚 Mis Cursos</h1>
          <hr style={{border: '0', borderTop: '1px solid #e2e8f0', marginBottom: '20px'}}/>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px'}}>
            <div style={{padding: '20px', border: '1px solid #ddd', borderRadius: '10px'}}>Matemáticas Aplicadas</div>
            <div style={{padding: '20px', border: '1px solid #ddd', borderRadius: '10px'}}>Desarrollo Web con Django</div>
          </div>
        </div>
      );
      case 'notas': return <div><h1 style={{fontSize: '32px'}}>📊 Calificaciones</h1><p>No hay notas registradas en este periodo.</p></div>;
      default: return (
        <>
          <h1 style={{fontSize: '32px', fontWeight: '800', margin: '0 0 10px 0'}}>Panel General</h1>
          <p style={{color: '#64748b', marginBottom: '40px'}}>Bienvenido al sistema central de INFO CAMPUS.</p>
          
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '25px'}}>
            <div style={{backgroundColor: 'white', padding: '25px', borderRadius: '16px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'}}>
              <h4 style={{color: '#64748b', margin: '0 0 15px 0', fontSize: '14px', textTransform: 'uppercase'}}>Asistencia Promedio</h4>
              <p style={{fontSize: '36px', fontWeight: 'bold', margin: 0, color: '#0f172a'}}>94.2%</p>
            </div>
            <div style={{backgroundColor: 'white', padding: '25px', borderRadius: '16px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'}}>
              <h4 style={{color: '#64748b', margin: '0 0 15px 0', fontSize: '14px', textTransform: 'uppercase'}}>Créditos Aprobados</h4>
              <p style={{fontSize: '36px', fontWeight: 'bold', margin: 0, color: '#cc0000'}}>120</p>
            </div>
          </div>
        </>
      );
    }
  };

  return (
    <div style={styles.container}>
      {/* 1. SIDEBAR IZQUIERDO */}
      <aside style={styles.sidebar}>
        <div style={styles.logoSection}>
          INFO<span style={{color: '#cc0000'}}>CAMPUS</span>
        </div>
        <nav style={styles.menu}>
          <div style={styles.menuItem('dashboard')} onClick={() => setActiveTab('dashboard')}>
            <LayoutDashboard size={20} style={{marginRight: '15px'}} /> Inicio
          </div>
          <div style={styles.menuItem('cursos')} onClick={() => setActiveTab('cursos')}>
            <BookOpen size={20} style={{marginRight: '15px'}} /> Mis Cursos
          </div>
          <div style={styles.menuItem('notas')} onClick={() => setActiveTab('notas')}>
            <GraduationCap size={20} style={{marginRight: '15px'}} /> Calificaciones
          </div>
          <div style={styles.menuItem('config')} onClick={() => setActiveTab('config')}>
            <Settings size={20} style={{marginRight: '15px'}} /> Ajustes
          </div>
        </nav>
        <div style={{padding: '25px', borderTop: '1px solid #1e293b'}}>
          <button onClick={onLogout} style={{display: 'flex', alignItems: 'center', width: '100%', background: 'none', border: 'none', color: '#f87171', cursor: 'pointer', fontSize: '15px', fontWeight: '600'}}>
            <LogOut size={18} style={{marginRight: '12px'}} /> Salir del Portal
          </button>
        </div>
      </aside>

      {/* 2. CONTENIDO DERECHO (TODO EL RESTO) */}
      <div style={styles.mainWrapper}>
        <header style={styles.header}>
          <div style={{color: '#64748b', fontSize: '14px', fontWeight: '500'}}>
            {activeTab.toUpperCase()} / VISUALIZACIÓN GENERAL
          </div>
          
          <div style={{display: 'flex', alignItems: 'center', gap: '25px'}}>
            <Bell size={20} color="#64748b" style={{cursor: 'pointer'}} />
            <div style={styles.userProfile}>
              <div style={{textAlign: 'right'}}>
                <div style={{fontSize: '14px', fontWeight: '700', color: '#1e293b'}}>{user.nombre}</div>
                <div style={{fontSize: '11px', color: '#cc0000', fontWeight: '800', textTransform: 'uppercase'}}>{user.rol}</div>
              </div>
              <div style={{width: '35px', height: '35px', backgroundColor: '#cc0000', borderRadius: '50%', display: 'flex', justifyContent: 'center', alignItems: 'center', color: 'white'}}>
                <UserIcon size={20} />
              </div>
            </div>
          </div>
        </header>

        <div style={styles.bodyLayout}>
          {/* ÁREA DE TRABAJO DINÁMICA */}
          <section style={styles.contentScroll}>
            <RenderContent />
          </section>

          {/* PANEL LATERAL DE INFORMACIÓN ÚTIL */}
          <aside style={styles.rightPanel}>
            <h3 style={{fontSize: '18px', marginBottom: '25px', display: 'flex', alignItems: 'center', gap: '10px'}}>
              <Calendar size={20} color="#cc0000" /> Agenda de Hoy
            </h3>
            
            <div style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
              <div style={{padding: '15px', backgroundColor: '#f8fafc', borderRadius: '12px', borderLeft: '4px solid #cc0000'}}>
                <div style={{fontSize: '12px', color: '#64748b'}}>08:00 AM - 10:00 AM</div>
                <div style={{fontWeight: '700', fontSize: '14px'}}>Sistemas Distribuidos</div>
                <div style={{fontSize: '12px', color: '#94a3b8'}}>Aula 402 - Edificio B</div>
              </div>

              <div style={{padding: '15px', backgroundColor: '#f8fafc', borderRadius: '12px', borderLeft: '4px solid #94a3b8'}}>
                <div style={{fontSize: '12px', color: '#64748b'}}>10:30 AM - 12:30 PM</div>
                <div style={{fontWeight: '700', fontSize: '14px'}}>Taller de Ética</div>
                <div style={{fontSize: '12px', color: '#94a3b8'}}>Auditorio Principal</div>
              </div>
            </div>

            <div style={{marginTop: '40px', padding: '20px', backgroundColor: '#fff1f2', borderRadius: '15px'}}>
              <h4 style={{margin: '0 0 10px 0', color: '#991b1b', fontSize: '14px'}}>Aviso Institucional</h4>
              <p style={{fontSize: '12px', color: '#991b1b', lineHeight: '1.5'}}>
                El sistema de pagos estará en mantenimiento este sábado a las 22:00.
              </p>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;