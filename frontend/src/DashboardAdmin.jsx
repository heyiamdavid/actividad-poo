import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, GraduationCap, Building2, BookOpen, BookText, LogOut, FileText, UserPlus } from 'lucide-react';

export default function DashboardAdmin() {
  const [activeTab, setActiveTab] = useState('estudiantes');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          Sig<span>Ma</span>
        </div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>
          PANEL ADMINISTRADOR
        </div>

        <nav>
          <div 
            className={`nav-item ${activeTab === 'estudiantes' ? 'active' : ''}`}
            onClick={() => setActiveTab('estudiantes')}
          >
            <Users size={20} />
            Estudiantes
          </div>
          <div 
            className={`nav-item ${activeTab === 'profesores' ? 'active' : ''}`}
            onClick={() => setActiveTab('profesores')}
          >
            <GraduationCap size={20} />
            Profesores
          </div>
          <div 
            className={`nav-item ${activeTab === 'universidades' ? 'active' : ''}`}
            onClick={() => setActiveTab('universidades')}
          >
            <Building2 size={20} />
            Universidades
          </div>
          <div 
            className={`nav-item ${activeTab === 'carreras' ? 'active' : ''}`}
            onClick={() => setActiveTab('carreras')}
          >
            <BookOpen size={20} />
            Carreras
          </div>
          <div 
            className={`nav-item ${activeTab === 'cursos' ? 'active' : ''}`}
            onClick={() => setActiveTab('cursos')}
          >
            <BookText size={20} />
            Cursos
          </div>
          <div 
            className={`nav-item ${activeTab === 'reportes' ? 'active' : ''}`}
            onClick={() => setActiveTab('reportes')}
          >
            <FileText size={20} />
            Reportes
          </div>
        </nav>

        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" onClick={handleLogout} style={{ color: 'var(--danger)' }}>
            <LogOut size={20} />
            Cerrar Sesion
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
            {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Gestiona la informacion del sistema universitario.</p>
        </header>

        {activeTab === 'estudiantes' && (
          <div className="animate-fade-in">
            <div className="dashboard-grid">
              <div className="glass stat-card">
                <div className="stat-icon"><Users size={24} /></div>
                <div className="stat-info">
                  <h3>--</h3>
                  <p>Total Estudiantes</p>
                </div>
              </div>
            </div>
            <div className="glass" style={{ padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Lista de Estudiantes</h2>
                <button className="btn btn-primary"><UserPlus size={18} /> Registrar Estudiante</button>
              </div>
              <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
                Funcionalidad de tabla en construccion...
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profesores' && (
          <div className="animate-fade-in">
            <div className="dashboard-grid">
              <div className="glass stat-card">
                <div className="stat-icon"><GraduationCap size={24} /></div>
                <div className="stat-info">
                  <h3>--</h3>
                  <p>Total Profesores</p>
                </div>
              </div>
            </div>
            <div className="glass" style={{ padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Lista de Profesores</h2>
                <button className="btn btn-primary"><UserPlus size={18} /> Registrar Profesor</button>
              </div>
              <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
                Funcionalidad de tabla en construccion...
              </div>
            </div>
          </div>
        )}

        {/* Placeholder para otras pestañas */}
        {['universidades', 'carreras', 'cursos', 'reportes'].includes(activeTab) && (
          <div className="animate-fade-in glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Modulo de {activeTab} en construccion...
          </div>
        )}
      </main>
    </div>
  );
}
