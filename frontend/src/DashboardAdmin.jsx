import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, GraduationCap, BookOpen, BookText, LogOut, UserPlus, Plus, Building2, Landmark, Edit, Trash2, Link } from 'lucide-react';

export default function DashboardAdmin() {
  const [activeTab, setActiveTab] = useState('estudiantes');
  
  const [estudiantes, setEstudiantes] = useState([]);
  const [profesores, setProfesores] = useState([]);
  const [carreras, setCarreras] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [sedes, setSedes] = useState([]);
  const [facultades, setFacultades] = useState([]);
  
  const [stats, setStats] = useState({ total_estudiantes: '--', total_profesores: '--' });
  const [loading, setLoading] = useState(false);
  
  const [showProfForm, setShowProfForm] = useState(false);
  const [showCursoForm, setShowCursoForm] = useState(false);
  const [showEstForm, setShowEstForm] = useState(false);
  const [showSedeForm, setShowSedeForm] = useState(false);
  const [showFacForm, setShowFacForm] = useState(false);
  const [showCarForm, setShowCarForm] = useState(false);
  const [showAsignarForm, setShowAsignarForm] = useState(false);
  
  const [editingEstudiante, setEditingEstudiante] = useState(null);
  const [editingProfesor, setEditingProfesor] = useState(null);

  const [profForm, setProfForm] = useState({ nombre: '', telefono: '', email: '', identificacion: '', titulo: '' });
  const [cursoForm, setCursoForm] = useState({ codigo_carrera: '', codigo_curso: '', nombre_curso: '', creditos: 3, semestre: 1, dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', numero_aula: '101', capacidad_aula: 30 });
  const [estudianteForm, setEstudianteForm] = useState({
    nombre: '', telefono: '', email: '', identificacion: '', contrasena: '',
    promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo',
    modalidad: 'Presencial', codigo_carrera: '', semestre: 1
  });
  const [sedeForm, setSedeForm] = useState({ nombre_sede: '', direccion: '', ciudad: '' });
  const [facForm, setFacForm] = useState({ nombre_sede: '', id_facultad: '', nombre_facultad: '' });
  const [carForm, setCarForm] = useState({ id_facultad: '', codigo_carrera: '', nombre_carrera: '', modalidad: 'Presencial' });
  const [asignarForm, setAsignarForm] = useState({ identificacion_profesor: '', codigo_curso: '' });

  const navigate = useNavigate();

  function generarClave() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return Array.from({ length: 6 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
  }

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  useEffect(() => {
    fetchStats();
    if (activeTab === 'estudiantes') { fetchEstudiantes(); fetchCarreras(); }
    if (activeTab === 'profesores') fetchProfesores();
    if (activeTab === 'carreras') { fetchCarreras(); fetchFacultades(); }
    if (activeTab === 'cursos') { fetchCursos(); fetchProfesores(); }
    if (activeTab === 'sedes') fetchSedes();
    if (activeTab === 'facultades') { fetchFacultades(); fetchSedes(); }
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

  async function fetchSedes() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/sedes');
      const data = await res.json();
      if (res.ok && data.status === 'success') setSedes(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  async function fetchFacultades() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/admin/facultades');
      const data = await res.json();
      if (res.ok && data.status === 'success') setFacultades(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }

  // --- HANDLERS ESTUDIANTES ---
  async function handleCreateEstudiante(e) {
    e.preventDefault();
    if (editingEstudiante) {
      try {
        const res = await fetch(`http://localhost:8000/api/admin/estudiantes/${editingEstudiante.identificacion}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            nombre: estudianteForm.nombre,
            telefono: estudianteForm.telefono,
            email: estudianteForm.email,
            estado: estudianteForm.estado,
            modalidad: estudianteForm.modalidad,
            semestre: parseInt(estudianteForm.semestre)
          })
        });
        if (res.ok) {
          alert('Estudiante actualizado exitosamente');
          setShowEstForm(false);
          setEditingEstudiante(null);
          setEstudianteForm({ nombre: '', telefono: '', email: '', identificacion: '', contrasena: '', promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo', modalidad: 'Presencial', codigo_carrera: '', semestre: 1 });
          fetchEstudiantes();
        } else alert("Error al actualizar estudiante");
      } catch(e) { console.error(e); alert('Error de red'); }
    } else {
      const claveGenerada = estudianteForm.contrasena;
      try {
        const res = await fetch('http://localhost:8000/api/admin/estudiantes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...estudianteForm,
            contrasena: claveGenerada,
            promedio_ingreso: parseFloat(estudianteForm.promedio_ingreso),
            promedio_graduacion: parseFloat(estudianteForm.promedio_graduacion),
            semestre: parseInt(estudianteForm.semestre)
          })
        });
        const data = await res.json();
        if (res.ok) {
          alert(`Estudiante registrado exitosamente.\n\nClave temporal asignada: ${claveGenerada}${data.en_nivelacion ? '\nEl estudiante fue asignado a nivelación por promedio bajo.' : ''}\n\nDeberá cambiarla al iniciar sesión.`);
          setShowEstForm(false);
          setEstudianteForm({ nombre: '', telefono: '', email: '', identificacion: '', contrasena: '', promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo', modalidad: 'Presencial', codigo_carrera: '', semestre: 1 });
          fetchEstudiantes();
          fetchStats();
        } else alert('Error: ' + (data.detail || 'Error al registrar estudiante'));
      } catch(e) { console.error(e); alert('Error de red'); }
    }
  }

  async function handleDeleteEstudiante(identificacion) {
    if (!window.confirm('¿Seguro que deseas eliminar este estudiante?')) return;
    try {
      const res = await fetch(`http://localhost:8000/api/admin/estudiantes/${identificacion}`, { method: 'DELETE' });
      if (res.ok) { fetchEstudiantes(); fetchStats(); }
      else alert("Error al eliminar estudiante");
    } catch(e) { console.error(e); }
  }

  // --- HANDLERS PROFESORES ---
  async function handleCreateProfesor(e) {
    e.preventDefault();
    if (editingProfesor) {
      try {
        const res = await fetch(`http://localhost:8000/api/admin/profesores/${editingProfesor.identificacion}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            nombre: profForm.nombre,
            telefono: profForm.telefono,
            email: profForm.email,
            titulo: profForm.titulo
          })
        });
        if (res.ok) {
          alert('Profesor actualizado exitosamente');
          setShowProfForm(false);
          setEditingProfesor(null);
          setProfForm({ nombre: '', telefono: '', email: '', identificacion: '', titulo: '', contrasena: '' });
          fetchProfesores();
        } else alert("Error al actualizar profesor");
      } catch(e) { console.error(e); alert('Error de red'); }
    } else {
      const claveGenerada = profForm.contrasena;
      try {
        const res = await fetch('http://localhost:8000/api/admin/profesores', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ...profForm, contrasena: claveGenerada })
        });
        if (res.ok) {
          alert(`Profesor registrado exitosamente.\n\nClave temporal asignada: ${claveGenerada}\n\nDeberá cambiarla al iniciar sesión.`);
          setShowProfForm(false);
          setProfForm({ nombre: '', telefono: '', email: '', identificacion: '', titulo: '', contrasena: '' });
          fetchProfesores();
          fetchStats();
        } else alert("Error al registrar profesor");
      } catch(e) { console.error(e); alert("Error de red"); }
    }
  }

  async function handleDeleteProfesor(identificacion) {
    if (!window.confirm('¿Seguro que deseas eliminar este profesor?')) return;
    try {
      const res = await fetch(`http://localhost:8000/api/admin/profesores/${identificacion}`, { method: 'DELETE' });
      if (res.ok) { fetchProfesores(); fetchStats(); }
      else alert("Error al eliminar profesor");
    } catch(e) { console.error(e); }
  }

  // --- HANDLERS UNIVERSIDAD ---
  async function handleCreateSede(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/sedes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sedeForm)
      });
      if (res.ok) {
        setShowSedeForm(false);
        setSedeForm({ nombre_sede: '', direccion: '', ciudad: '' });
        fetchSedes();
      } else alert("Error al registrar sede");
    } catch(e) { console.error(e); }
  }

  async function handleCreateFacultad(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/facultades', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...facForm, id_facultad: parseInt(facForm.id_facultad)})
      });
      if (res.ok) {
        setShowFacForm(false);
        setFacForm({ nombre_sede: '', id_facultad: '', nombre_facultad: '' });
        fetchFacultades();
      } else alert("Error al registrar facultad");
    } catch(e) { console.error(e); }
  }

  async function handleCreateCarrera(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/carreras', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...carForm, id_facultad: parseInt(carForm.id_facultad)})
      });
      if (res.ok) {
        setShowCarForm(false);
        setCarForm({ id_facultad: '', codigo_carrera: '', nombre_carrera: '', modalidad: 'Presencial' });
        fetchCarreras();
      } else alert("Error al registrar carrera");
    } catch(e) { console.error(e); }
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
      } else alert("Error al registrar curso. Verifique que el código de carrera exista.");
    } catch(e) { console.error(e); alert("Error de red"); }
  }

  async function handleAsignarCurso(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/admin/asignar_curso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(asignarForm)
      });
      if (res.ok) {
        alert("Curso asignado a profesor exitosamente.");
        setShowAsignarForm(false);
        setAsignarForm({ identificacion_profesor: '', codigo_curso: '' });
      } else {
        const data = await res.json();
        alert(data.detail || "Error al asignar curso");
      }
    } catch(e) { console.error(e); }
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">Sig<span>Ma</span></div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>PANEL ADMINISTRADOR</div>
        <nav>
          <div className={`nav-item ${activeTab === 'estudiantes' ? 'active' : ''}`} onClick={() => setActiveTab('estudiantes')}><Users size={20} /> Estudiantes</div>
          <div className={`nav-item ${activeTab === 'profesores' ? 'active' : ''}`} onClick={() => setActiveTab('profesores')}><GraduationCap size={20} /> Profesores</div>
          <div className={`nav-item ${activeTab === 'sedes' ? 'active' : ''}`} onClick={() => setActiveTab('sedes')}><Building2 size={20} /> Sedes</div>
          <div className={`nav-item ${activeTab === 'facultades' ? 'active' : ''}`} onClick={() => setActiveTab('facultades')}><Landmark size={20} /> Facultades</div>
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
                <button className="btn btn-primary" onClick={() => {
                  if (!showEstForm) {
                    setEditingEstudiante(null);
                    setEstudianteForm({ nombre: '', telefono: '', email: '', identificacion: '', contrasena: generarClave(), promedio_ingreso: 7.0, promedio_graduacion: 7.0, estado: 'Activo', modalidad: 'Presencial', codigo_carrera: '', semestre: 1 });
                  }
                  setShowEstForm(!showEstForm);
                }}>
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
                    <input type="text" className="form-input" placeholder="Número de ID" required disabled={!!editingEstudiante} value={estudianteForm.identificacion} onChange={e => setEstudianteForm({...estudianteForm, identificacion: e.target.value})} />
                  </div>
                  
                  {!editingEstudiante && (
                    <div className="form-group">
                      <label style={{ color: 'var(--primary)', fontWeight: 'bold' }}>Clave Temporal (Generada)</label>
                      <input type="text" className="form-input" readOnly value={estudianteForm.contrasena || ''} style={{ background: 'rgba(99,102,241,0.1)', cursor: 'copy', userSelect: 'all' }} title="Copia esta clave" />
                    </div>
                  )}

                  <div className="form-group">
                    <label>Email</label>
                    <input type="email" className="form-input" placeholder="correo@ejemplo.com" required value={estudianteForm.email} onChange={e => setEstudianteForm({...estudianteForm, email: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Teléfono</label>
                    <input type="text" className="form-input" placeholder="Número de teléfono" required value={estudianteForm.telefono} onChange={e => setEstudianteForm({...estudianteForm, telefono: e.target.value})} />
                  </div>
                  
                  {!editingEstudiante && (
                    <>
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
                    </>
                  )}

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
                  {!editingEstudiante && (
                    <p style={{ gridColumn: 'span 2', color: 'var(--text-muted)', fontSize: '0.85rem', margin: 0 }}>
                       Si el promedio combinado es menor a 8.0, el estudiante será asignado automáticamente a nivelación.
                    </p>
                  )}
                  <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>
                    {editingEstudiante ? 'Guardar Cambios' : 'Registrar Estudiante'}
                  </button>
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
                    <th style={{ padding: '12px', color: 'var(--text-muted)' }}>Acciones</th>
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
                        <td style={{ padding: '12px', display: 'flex', gap: '10px' }}>
                          <button style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer' }} onClick={() => {
                            setEditingEstudiante(e);
                            setEstudianteForm({ ...e, contrasena: '' });
                            setShowEstForm(true);
                          }}><Edit size={16} /></button>
                          <button style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }} onClick={() => handleDeleteEstudiante(e.identificacion)}><Trash2 size={16} /></button>
                        </td>
                      </tr>
                    ))}
                    {estudiantes.length === 0 && <tr><td colSpan="7" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>No hay estudiantes registrados</td></tr>}
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
                <button className="btn btn-primary" onClick={() => {
                  if (!showProfForm) {
                    setEditingProfesor(null);
                    setProfForm({ nombre: '', telefono: '', email: '', identificacion: '', titulo: '', contrasena: generarClave() });
                  }
                  setShowProfForm(!showProfForm);
                }}>
                  <UserPlus size={18} /> {showProfForm ? 'Cancelar' : 'Registrar Profesor'}
                </button>
              </div>

              {showProfForm && (
                <form onSubmit={handleCreateProfesor} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                  <input type="text" className="form-input" placeholder="Nombre" required value={profForm.nombre} onChange={e => setProfForm({...profForm, nombre: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Identificacion" disabled={!!editingProfesor} required value={profForm.identificacion} onChange={e => setProfForm({...profForm, identificacion: e.target.value})} />
                  <input type="email" className="form-input" placeholder="Email" required value={profForm.email} onChange={e => setProfForm({...profForm, email: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Telefono" required value={profForm.telefono} onChange={e => setProfForm({...profForm, telefono: e.target.value})} />
                  <input type="text" className="form-input" placeholder="Titulo" required value={profForm.titulo} onChange={e => setProfForm({...profForm, titulo: e.target.value})} />
                  
                  {!editingProfesor && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                      <label style={{ fontSize: '0.8rem', color: 'var(--primary)', fontWeight: 'bold' }}>Clave Temporal (Generada)</label>
                      <input type="text" className="form-input" readOnly value={profForm.contrasena || ''} style={{ background: 'rgba(99,102,241,0.1)', cursor: 'copy', userSelect: 'all' }} title="Copia esta clave" />
                    </div>
                  )}
                  <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>
                    {editingProfesor ? 'Guardar Cambios' : 'Guardar Profesor'}
                  </button>
                </form>
              )}

              {loading ? <p>Cargando...</p> : (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>ID</th><th>Nombre</th><th>Email</th><th>Titulo</th><th>Acciones</th></tr></thead>
                  <tbody>
                    {profesores.map(p => (
                      <tr key={p.identificacion} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '12px' }}>{p.identificacion}</td>
                        <td style={{ padding: '12px' }}>{p.nombre}</td>
                        <td style={{ padding: '12px' }}>{p.email}</td>
                        <td style={{ padding: '12px' }}>{p.titulo}</td>
                        <td style={{ padding: '12px', display: 'flex', gap: '10px' }}>
                          <button style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer' }} onClick={() => {
                            setEditingProfesor(p);
                            setProfForm({ ...p, contrasena: '' });
                            setShowProfForm(true);
                          }}><Edit size={16} /></button>
                          <button style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }} onClick={() => handleDeleteProfesor(p.identificacion)}><Trash2 size={16} /></button>
                        </td>
                      </tr>
                    ))}
                    {profesores.length === 0 && <tr><td colSpan="5" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>No hay profesores registrados</td></tr>}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {activeTab === 'sedes' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2>Lista de Sedes</h2>
              <button className="btn btn-primary" onClick={() => setShowSedeForm(!showSedeForm)}>
                <Plus size={18} /> {showSedeForm ? 'Cancelar' : 'Crear Sede'}
              </button>
            </div>
            {showSedeForm && (
              <form onSubmit={handleCreateSede} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <input type="text" className="form-input" placeholder="Nombre Sede" required value={sedeForm.nombre_sede} onChange={e => setSedeForm({...sedeForm, nombre_sede: e.target.value})} />
                <input type="text" className="form-input" placeholder="Ciudad" required value={sedeForm.ciudad} onChange={e => setSedeForm({...sedeForm, ciudad: e.target.value})} />
                <input type="text" className="form-input" placeholder="Dirección" required value={sedeForm.direccion} onChange={e => setSedeForm({...sedeForm, direccion: e.target.value})} style={{ gridColumn: 'span 2' }} />
                <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Sede</button>
              </form>
            )}
            {loading ? <p>Cargando...</p> : (
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginTop: '20px' }}>
                <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>Sede</th><th>Ciudad</th><th>Dirección</th></tr></thead>
                <tbody>
                  {sedes.map(s => (
                    <tr key={s.nombre_sede} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px' }}>{s.nombre_sede}</td>
                      <td style={{ padding: '12px' }}>{s.ciudad}</td>
                      <td style={{ padding: '12px' }}>{s.direccion}</td>
                    </tr>
                  ))}
                  {sedes.length === 0 && <tr><td colSpan="3" style={{ padding: '20px', textAlign: 'center' }}>No hay sedes</td></tr>}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'facultades' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2>Lista de Facultades</h2>
              <button className="btn btn-primary" onClick={() => setShowFacForm(!showFacForm)}>
                <Plus size={18} /> {showFacForm ? 'Cancelar' : 'Crear Facultad'}
              </button>
            </div>
            {showFacForm && (
              <form onSubmit={handleCreateFacultad} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <select className="form-input" required value={facForm.nombre_sede} onChange={e => setFacForm({...facForm, nombre_sede: e.target.value})}>
                  <option value="">Seleccione Sede</option>
                  {sedes.map(s => <option key={s.nombre_sede} value={s.nombre_sede}>{s.nombre_sede}</option>)}
                </select>
                <input type="number" className="form-input" placeholder="ID Facultad" required value={facForm.id_facultad} onChange={e => setFacForm({...facForm, id_facultad: e.target.value})} />
                <input type="text" className="form-input" placeholder="Nombre Facultad" required value={facForm.nombre_facultad} onChange={e => setFacForm({...facForm, nombre_facultad: e.target.value})} style={{ gridColumn: 'span 2' }} />
                <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Facultad</button>
              </form>
            )}
            {loading ? <p>Cargando...</p> : (
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginTop: '20px' }}>
                <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>ID</th><th>Nombre</th><th>Sede</th></tr></thead>
                <tbody>
                  {facultades.map(f => (
                    <tr key={f.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px' }}>{f.id}</td>
                      <td style={{ padding: '12px' }}>{f.nombre}</td>
                      <td style={{ padding: '12px' }}>{f.sede}</td>
                    </tr>
                  ))}
                  {facultades.length === 0 && <tr><td colSpan="3" style={{ padding: '20px', textAlign: 'center' }}>No hay facultades</td></tr>}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'carreras' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2>Lista de Carreras</h2>
              <button className="btn btn-primary" onClick={() => setShowCarForm(!showCarForm)}>
                <Plus size={18} /> {showCarForm ? 'Cancelar' : 'Crear Carrera'}
              </button>
            </div>
            
            {showCarForm && (
              <form onSubmit={handleCreateCarrera} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <select className="form-input" required value={carForm.id_facultad} onChange={e => setCarForm({...carForm, id_facultad: e.target.value})}>
                  <option value="">Seleccione Facultad</option>
                  {facultades.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                </select>
                <input type="text" className="form-input" placeholder="Código (ej. INFO)" required value={carForm.codigo_carrera} onChange={e => setCarForm({...carForm, codigo_carrera: e.target.value})} />
                <input type="text" className="form-input" placeholder="Nombre Carrera" required value={carForm.nombre_carrera} onChange={e => setCarForm({...carForm, nombre_carrera: e.target.value})} />
                <select className="form-input" required value={carForm.modalidad} onChange={e => setCarForm({...carForm, modalidad: e.target.value})}>
                  <option>Presencial</option>
                  <option>Semipresencial</option>
                  <option>Virtual</option>
                </select>
                <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Carrera</button>
              </form>
            )}

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
                  {carreras.length === 0 && <tr><td colSpan="3" style={{ padding: '20px', textAlign: 'center' }}>No hay carreras</td></tr>}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'cursos' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <div style={{ display: 'flex', gap: '15px', marginBottom: '20px' }}>
              <button className="btn btn-primary" onClick={() => { setShowCursoForm(!showCursoForm); setShowAsignarForm(false); }}>
                <Plus size={18} /> {showCursoForm ? 'Cancelar Curso' : 'Crear Curso'}
              </button>
              <button className="btn btn-primary" style={{ background: 'var(--accent)' }} onClick={() => { setShowAsignarForm(!showAsignarForm); setShowCursoForm(false); }}>
                <Link size={18} /> {showAsignarForm ? 'Cancelar Asignación' : 'Asignar a Profesor'}
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

            {showAsignarForm && (
              <form onSubmit={handleAsignarCurso} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                <select className="form-input" required value={asignarForm.identificacion_profesor} onChange={e => setAsignarForm({...asignarForm, identificacion_profesor: e.target.value})}>
                  <option value="">Seleccione Profesor</option>
                  {profesores.map(p => <option key={p.identificacion} value={p.identificacion}>{p.nombre}</option>)}
                </select>
                <select className="form-input" required value={asignarForm.codigo_curso} onChange={e => setAsignarForm({...asignarForm, codigo_curso: e.target.value})}>
                  <option value="">Seleccione Curso</option>
                  {cursos.map(c => <option key={c.codigo} value={c.codigo}>{c.nombre} ({c.codigo})</option>)}
                </select>
                <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2', background: 'var(--accent)' }}>Asignar Curso</button>
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
                  {cursos.length === 0 && <tr><td colSpan="4" style={{ padding: '20px', textAlign: 'center' }}>No hay cursos</td></tr>}
                </tbody>
              </table>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
