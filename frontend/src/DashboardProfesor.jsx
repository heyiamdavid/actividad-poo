import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, ClipboardList, PenTool, ListChecks, LogOut, GraduationCap } from 'lucide-react';

export default function DashboardProfesor() {
  const [activeTab, setActiveTab] = useState('datos');
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (!stored) {
      navigate('/login');
    } else {
      const parsed = JSON.parse(stored);
      if (parsed.rol !== 'profesor') navigate('/login');
      else setUser(parsed);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (!user) return null;

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          Sig<span>Ma</span>
        </div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>
          PANEL PROFESOR
        </div>

        <nav>
          <div 
            className={`nav-item ${activeTab === 'datos' ? 'active' : ''}`}
            onClick={() => setActiveTab('datos')}
          >
            <User size={20} />
            Ver Datos
          </div>
          <div 
            className={`nav-item ${activeTab === 'crear_evaluacion' ? 'active' : ''}`}
            onClick={() => setActiveTab('crear_evaluacion')}
          >
            <ClipboardList size={20} />
            Crear Evaluacion
          </div>
          <div 
            className={`nav-item ${activeTab === 'registrar_nota' ? 'active' : ''}`}
            onClick={() => setActiveTab('registrar_nota')}
          >
            <PenTool size={20} />
            Registrar Nota
          </div>
          <div 
            className={`nav-item ${activeTab === 'ver_evaluaciones' ? 'active' : ''}`}
            onClick={() => setActiveTab('ver_evaluaciones')}
          >
            <ListChecks size={20} />
            Ver Evaluaciones
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
            {activeTab === 'datos' ? 'Mis Datos' : 
             activeTab === 'crear_evaluacion' ? 'Nueva Evaluacion' :
             activeTab === 'registrar_nota' ? 'Calificar Alumnos' : 'Historial de Evaluaciones'}
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Bienvenido, {user.nombre}</p>
        </header>

        {activeTab === 'datos' && (
          <div className="animate-fade-in glass" style={{ padding: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px' }}>
              <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(99,102,241,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <GraduationCap size={40} />
              </div>
              <div>
                <h2 style={{ fontSize: '1.8rem', margin: 0 }}>{user.nombre}</h2>
                <p style={{ color: 'var(--text-muted)', margin: 0 }}>Profesor Titular</p>
              </div>
            </div>
            
            <div className="dashboard-grid">
               <div className="form-group">
                 <label>Identificacion</label>
                 <div className="form-input" style={{ opacity: 0.7 }}>{user.identificacion}</div>
               </div>
            </div>
          </div>
        )}

        {['crear_evaluacion', 'registrar_nota', 'ver_evaluaciones'].includes(activeTab) && (
          <div className="animate-fade-in glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Modulo de {activeTab.replace('_', ' ')} en construccion...
          </div>
        )}
      </main>
    </div>
  );
}
