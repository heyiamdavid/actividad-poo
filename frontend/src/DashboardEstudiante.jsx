import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Library, GraduationCap, Award, LogOut } from 'lucide-react';

export default function DashboardEstudiante() {
  const [activeTab, setActiveTab] = useState('datos');
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (!stored) {
      navigate('/login');
    } else {
      const parsed = JSON.parse(stored);
      if (parsed.rol !== 'estudiante') navigate('/login');
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
          PANEL ESTUDIANTE
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
            className={`nav-item ${activeTab === 'cursos' ? 'active' : ''}`}
            onClick={() => setActiveTab('cursos')}
          >
            <Library size={20} />
            Consultar Cursos
          </div>
          <div 
            className={`nav-item ${activeTab === 'modalidad' ? 'active' : ''}`}
            onClick={() => setActiveTab('modalidad')}
          >
            <GraduationCap size={20} />
            Ver Modalidad
          </div>
          <div 
            className={`nav-item ${activeTab === 'notas' ? 'active' : ''}`}
            onClick={() => setActiveTab('notas')}
          >
            <Award size={20} />
            Ver Notas
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
            {activeTab === 'datos' ? 'Mi Perfil' : 
             activeTab === 'cursos' ? 'Mis Cursos' :
             activeTab === 'modalidad' ? 'Modalidad de Estudio' : 'Calificaciones'}
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Bienvenido, {user.nombre}</p>
        </header>

        {activeTab === 'datos' && (
          <div className="animate-fade-in glass" style={{ padding: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px' }}>
              <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(236, 72, 153, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--secondary)' }}>
                <User size={40} />
              </div>
              <div>
                <h2 style={{ fontSize: '1.8rem', margin: 0 }}>{user.nombre}</h2>
                <p style={{ color: 'var(--text-muted)', margin: 0 }}>Estudiante Activo</p>
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

        {['cursos', 'modalidad', 'notas'].includes(activeTab) && (
          <div className="animate-fade-in glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Modulo de {activeTab} en construccion...
          </div>
        )}
      </main>
    </div>
  );
}
