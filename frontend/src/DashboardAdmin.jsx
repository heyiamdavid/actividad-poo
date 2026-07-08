import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, GraduationCap, BookOpen, BookText, LogOut, UserPlus, Plus } from 'lucide-react';

export default function DashboardAdmin() {
  const [activeTab, setActiveTab] = useState('estudiantes');
  
  const [estudiantes, setEstudiantes] = useState([]);
  const [profesores, setProfesores] = useState([]);
  const [carreras, setCarreras] = useState([]);
  const [cursos, setCursos] = useState([]);
  
  const [stats, setStats] = useState({ total_estudiantes: '--', total_profesores: '--' });
  const [loading, setLoading] = useState(false);
  
  const [showProfForm, setShowProfForm] = useState(false);
  const [showCursoForm, setShowCursoForm] = useState(false);
  
  const [profForm, setProfForm] = useState({ nombre: '', telefono: '', email: '', identificacion: '', contrasena: '', titulo: '' });
  const [cursoForm, setCursoForm] = useState({ codigo_carrera: '', codigo_curso: '', nombre_curso: '', creditos: 3, semestre: 1, dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', numero_aula: '101', capacidad_aula: 30 });
  const [showEstForm, setShowEstForm] = useState(false);
  const [estudianteForm, setEstudianteForm] = useState({
    nombre: '', telefono: '', email: '', identificacion: '', contrasena: '',
    promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo',
    modalidad: 'Presencial', codigo_carrera: '', semestre: 1
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  useEffect(() => {
    fetchStats();
    if (activeTab === 'estudiantes') { fetchEstudiantes(); fetchCarreras(); }
    if (activeTab === 'profesores') fetchProfesores();
    if (activeTab === 'carreras') fetchCarreras();
    if (activeTab === 'cursos') fetchCursos();
  }, [activeTab]);

  async function fetchStats() {
    try {
      const res = await fetch('http://localhost:8000/api/admin/estadisticas');
      const data = await res.json();
      if (res.ok && data.status === 'success') setStats(data.data);
    } catch (e) { console.error(e); }
  }

  async function fetchEstudiantes() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/estudiantes');
      const data = await res.json();
      if (res.ok && data.status === 'success') setEstudiantes(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  async function fetchProfesores() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/profesores');
      const data = await res.json();
      if (res.ok && data.status === 'success') setProfesores(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  async function fetchCarreras() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/carreras');
      const data = await res.json();
      if (res.ok && data.status === 'success') setCarreras(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  async function fetchCursos() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/cursos');
      const data = await res.json();
      if (res.ok && data.status === 'success') setCursos(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  async function handleCreateProfesor(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/profesores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profForm)
      });
      if (res.ok) {
        setShowProfForm(false);
        fetchProfesores();
      } else {
        alert("Error al registrar profesor");
      }
    } catch(e) { 
      console.error(e);
      alert("Error de red"); 
    }
  }

  async function handleCreateCurso(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/cursos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cursoForm)
      });
      if (res.ok) {
        setShowCursoForm(false);
        fetchCursos();
      } else {
        alert("Error al registrar curso. Verifique que el código de carrera exista.");
      }
    } catch(e) { 
      console.error(e);
      alert("Error de red"); 
    }
  }

  async function handleCreateEstudiante(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/estudiantes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...estudianteForm,
          promedio_ingreso: parseFloat(estudianteForm.promedio_ingreso),
          promedio_graduacion: parseFloat(estudianteForm.promedio_graduacion),
          semestre: parseInt(estudianteForm.semestre)
        })
      });
      const data = await res.json();
      if (res.ok) {
        alert(data.message + (data.en_nivelacion ? '\n El estudiante fue asignado a nivelación por promedio bajo.' : ''));
        setShowEstForm(false);
        setEstudianteForm({ nombre: '', telefono: '', email: '', identificacion: '', contrasena: '', promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo', modalidad: 'Presencial', codigo_carrera: '', semestre: 1 });
        fetchEstudiantes();
        fetchStats();
      } else {
        alert('Error: ' + (data.detail || 'Error al registrar estudiante'));
      }
    } catch(e) { 
      console.error(e);
      alert('Error de red'); 
    }
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">Sig<span>Ma</span></div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>PANEL ADMINISTRADOR</div>
        <nav>
          <div className={`nav-item ${activeTab === 'estudiantes' ? 'active' : ''}`} onClick={() => setActiveTab('estudiantes')}><Users size={20} /> Estudiantes</div>
          <div className={`nav-item ${activeTab === 'profesores' ? 'active' : ''}`} onClick={() => setActiveTab('profesores')}><GraduationCap size={20} /> Profesores</div>
          <div className={`nav-item ${activeTab === 'carreras' ? 'active' : ''}`} onClick={() => setActiveTab('carreras')}><BookOpen size={20} /> Carreras</div>
          <div className={`nav-item ${activeTab === 'cursos' ? 'active' : ''}`} onClick={() => setActiveTab('cursos')}><BookText size={20} /> Cursos</div>
        </nav>
        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" onClick={handleLogout} style={{ color: 'var(--danger)' }}><LogOut size={20} /> Cerrar Sesion</div>
        </div>
      </aside>

      <main className="main-content">
        <header style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
          <p style={{ color: 'var(--text-muted)' }}>Gestiona la informacion del sistema universitario.</p>
        </header>

        {activeTab === 'estudiantes' && (
          <div className="animate-fade-in">
            <div className="dashboard-grid">
              <div className="glass stat-card">
                <div className="stat-icon"><Users size={24} /></div>
                <div className="stat-info">
                  <h3>{stats.total_estudiantes}</h3>
                  <p>Total Estudiantes</p>
                </div>
              </div>
            </div>
            <div className="glass" style={{ padding: '24px', marginTop: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Lista de Estudiantes</h2>
                <button className="btn btn-primary" onClick={() => setShowEstForm(!showEstForm)}>
                  <UserPlus size={18} /> {showEstForm ? 'Cancelar' : 'Registrar Estudiante'}
                </button>
              </div>

              {showEstForm && (
                <form onSubmit={handleCreateEstudiante} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                  <div className="form-group">
                    <label>Nombre</label>
                    <input type="text" className="form-input" placeholder="Nombre completo" required value={estudianteForm.nombre} onChange={e => setEstudianteForm({...estudianteForm, nombre: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Identificación</label>
                    <input type="text" className="form-input" placeholder="Número de ID" required value={estudianteForm.identificacion} onChange={e => setEstudianteForm({...estudianteForm, identificacion: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Email</label>
                    <input type="email" className="form-input" placeholder="correo@ejemplo.com" required value={estudianteForm.email} onChange={e => setEstudianteForm({...estudianteForm, email: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Teléfono</label>
                    <input type="text" className="form-input" placeholder="Número de teléfono" required value={estudianteForm.telefono} onChange={e => setEstudianteForm({...estudianteForm, telefono: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Contraseña</label>
                    <input type="password" className="form-input" placeholder="Contraseña" required value={estudianteForm.contrasena} onChange={e => setEstudianteForm({...estudianteForm, contrasena: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Código Carrera</label>
                    <select className="form-input" required value={estudianteForm.codigo_carrera} onChange={e => setEstudianteForm({...estudianteForm, codigo_carrera: e.target.value})}>
                      <option value="">Seleccione una carrera...</option>
                      {carreras.map(c => <option key={c.codigo} value={c.codigo}>{c.nombre} ({c.codigo})</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Promedio de Ingreso</label>
                    <input type="number" step="0.1" min="0" max="10" className="form-input" value={estudianteForm.promedio_ingreso} onChange={e => setEstudianteForm({...estudianteForm, promedio_ingreso: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Promedio de Graduación</label>
                    <input type="number" step="0.1" min="0" max="10" className="form-input" value={estudianteForm.promedio_graduacion} onChange={e => setEstudianteForm({...estudianteForm, promedio_graduacion: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Estado</label>
                    <select className="form-input" value={estudianteForm.estado} onChange={e => setEstudianteForm({...estudianteForm, estado: e.target.value})}>
                      <option>Activo</option>
                      <option>Inactivo</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Modalidad</label>
                    <select className="form-input" value={estudianteForm.modalidad} onChange={e => setEstudianteForm({...estudianteForm, modalidad: e.target.value})}>
                      <option>Presencial</option>
                      <option>Semipresencial</option>
                      <option>Virtual</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Semestre (si aplica)</label>
                    <input type="number" min="1" max="10" className="form-input" value={estudianteForm.semestre} onChange={e => setEstudianteForm({...estudianteForm, semestre: e.target.value})} />
                  </div>
                  <p style={{ gridColumn: 'span 2', color: 'var(--text-muted)', fontSize: '0.85rem', margin: 0 }}>
                     Si el promedio combinado es menor a 8.0, el estudiante será asignado automáticamente a nivelación.
                  </p>
                  <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Registrar Estudiante</button>
                </form>
              )}

              {loading ? <p style={{ color: 'var(--text-muted)' }}>Cargando...</p> : (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>ID</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Nombre</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Email</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Carrera</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Semestre</th>
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Estado</th>
                  </tr></thead>
                  <tbody>
                    {estudiantes.map(e => (
                      <tr key={e.identificacion} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '12px' }}>{e.identificacion}</td>
                        <td style={{ padding: '12px' }}>{e.nombre}</td>
                        <td style={{ padding: '12px' }}>{e.email}</td>
                        <td style={{ padding: '12px' }}>{e.carrera}</td>
                        <td style={{ padding: '12px' }}>{e.semestre === 0 ? ' Nivelación' : e.semestre}</td>
                        <td style={{ padding: '12px' }}>
                          <span style={{ padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem', backgroundColor: e.estado === 'Activo' ? 'rgba(46,204,113,0.2)' : 'rgba(231,76,60,0.2)', color: e.estado === 'Activo' ? '#2ecc71' : '#e74c3c' }}>
                            {e.estado}
                          </span>
                        </td>
                      </tr>
                    ))}
                    {estudiantes.length === 0 && <tr><td colSpan="6" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>No hay estudiantes registrados</td></tr>}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {activeTab === 'profesores' && (
          <div className="animate-fade-in">
             <div className="dashboard-grid">
              <div className="glass stat-card">
                <div className="stat-icon"><GraduationCap size={24} /></div>
                <div className="stat-info">
                  <h3>{stats.total_profesores}</h3>
                  <p>Total Profesores</p>
                </div>
              </div>
            </div>

            <div className="glass" style={{ padding: '24px', marginTop: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Lista de Profesores</h2>
                <button className="btn btn-primary" onClick={() => setShowProfForm(!showProfForm)}>
                  <UserPlus size={18} /> {showProfForm ? 'Cancelar' : 'Registrar Profesor'}
                </button>
              </div>

              {showProfForm && (
                <form onSubmit={handleCreateProfesor} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                  <input type="text" className="form-input" placeholder="Nombre" required value={profForm.nombre} onChange={e => setProfForm({...profForm, nombre: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Identificacion" required value={profForm.identificacion} onChange={e => setProfForm({...profForm, identificacion: e.target.value})} />
                  <input type="email" className="form-input" placeholder="Email" required value={profForm.email} onChange={e => setProfForm({...profForm, email: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Telefono" required value={profForm.telefono} onChange={e => setProfForm({...profForm, telefono: e.target.value})} />
                  <input type="password" className="form-input" placeholder="Contrasena" required value={profForm.contrasena} onChange={e => setProfForm({...profForm, contrasena: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Titulo" required value={profForm.titulo} onChange={e => setProfForm({...profForm, titulo: e.target.value})} />
                  <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Profesor</button>
                </form>
              )}

              {loading ? <p>Cargando...</p> : (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>ID</th><th>Nombre</th><th>Email</th><th>Titulo</th></tr></thead>
                  <tbody>
                    {profesores.map(p => (
                      <tr key={p.identificacion} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '12px' }}>{p.identificacion}</td>
                        <td style={{ padding: '12px' }}>{p.nombre}</td>
                        <td style={{ padding: '12px' }}>{p.email}</td>
                        <td style={{ padding: '12px' }}>{p.titulo}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {activeTab === 'carreras' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <h2>Lista de Carreras</h2>
            <p style={{ color: 'var(--text-muted)' }}>Para registrar carreras se debe hacer por terminal debido a la estructura de Sedes y Facultades, pero puedes ver las existentes aquí.</p>
            {loading ? <p>Cargando...</p> : (
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginTop: '20px' }}>
                <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>Codigo</th><th>Nombre</th><th>Modalidad</th></tr></thead>
                <tbody>
                  {carreras.map(c => (
                    <tr key={c.codigo} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px' }}>{c.codigo}</td>
                      <td style={{ padding: '12px' }}>{c.nombre}</td>
                      <td style={{ padding: '12px' }}>{c.modalidad}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'cursos' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2>Lista de Cursos</h2>
              <button className="btn btn-primary" onClick={() => setShowCursoForm(!showCursoForm)}>
                <Plus size={18} /> {showCursoForm ? 'Cancelar' : 'Crear Curso'}
              </button>
            </div>

            {showCursoForm && (
              <form onSubmit={handleCreateCurso} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <input type="text" className="form-input" placeholder="Código Carrera (Ej: INFO)" required value={cursoForm.codigo_carrera} onChange={e => setCursoForm({...cursoForm, codigo_carrera: e.target.value})} />
                <input type="text" className="form-input" placeholder="Código Curso (Ej: PRG1)" required value={cursoForm.codigo_curso} onChange={e => setCursoForm({...cursoForm, codigo_curso: e.target.value})} />
                <input type="text" className="form-input" placeholder="Nombre Curso" required value={cursoForm.nombre_curso} onChange={e => setCursoForm({...cursoForm, nombre_curso: e.target.value})} />
                <input type="number" className="form-input" placeholder="Semestre" required value={cursoForm.semestre} onChange={e => setCursoForm({...cursoForm, semestre: parseInt(e.target.value)})} />
                <input type="number" className="form-input" placeholder="Créditos" required value={cursoForm.creditos} onChange={e => setCursoForm({...cursoForm, creditos: parseInt(e.target.value)})} />
                <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Curso</button>
              </form>
            )}

            {loading ? <p>Cargando...</p> : (
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>Codigo</th><th>Nombre</th><th>Semestre</th><th>Creditos</th></tr></thead>
                <tbody>
                  {cursos.map(c => (
                    <tr key={c.codigo} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px' }}>{c.codigo}</td>
                      <td style={{ padding: '12px' }}>{c.nombre}</td>
                      <td style={{ padding: '12px' }}>{c.semestre}</td>
                      <td style={{ padding: '12px' }}>{c.creditos}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
