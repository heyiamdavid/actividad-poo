import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, PenTool, BookOpen, LogOut, GraduationCap, Eye, EyeOff, ShieldAlert, Calendar, MapPin, ChevronDown, ChevronRight, Users } from 'lucide-react';

export default function DashboardProfesor() {
  const [activeTab, setActiveTab] = useState('datos');
  
  // Recuperamos la sesion desde el localStorage y verificamos que el rol coincida
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    if (!stored) return null;
    const parsed = JSON.parse(stored);
    return parsed.rol === 'profesor' ? parsed : null;
  });
  const navigate = useNavigate();

  const [cursos, setCursos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cursosExpandidos, setCursosExpandidos] = useState({});

  // Formularios para las diferentes operaciones del dashboard
  const [notaForm, setNotaForm] = useState({ identificacion_estudiante: '', codigo_curso: '', nombre_evaluacion: 'Parcial 1', calificacion: '' });
  const [claveForm, setClaveForm] = useState({ actual: '', nueva: '', confirmacion: '' });
  const [cambiandoClave, setCambiandoClave] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [editandoDatos, setEditandoDatos] = useState(false);
  const [datosForm, setDatosForm] = useState({ telefono: user?.telefono || '', email: user?.email || '' });

  // Maneja la actualizacion del perfil del profesor en el backend
  const handleUpdateDatos = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:8000/api/profesor/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosForm)
      });
      if (res.ok) {
        alert('Datos actualizados');
        const updatedUser = { ...user, ...datosForm };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        window.location.reload();
      } else {
        alert('Error al actualizar datos');
      }
    } catch (e) { console.error(e); alert('Error de red'); }
  };

  const fetchCursos = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      // Obtenemos los cursos asignados al profesor junto con los alumnos inscritos
      const res = await fetch(`http://localhost:8000/api/profesor/${user.id}/cursos`);
      const data = await res.json();
      if (res.ok && data.status === 'success') setCursos(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }, [user]);

  // Redireccion si no hay sesion activa
  useEffect(() => {
    if (!user) { navigate('/login'); }
  }, [user, navigate]);

  // Carga inicial de datos cuando cambiamos a pestañas que lo requieren
  useEffect(() => {
    if (!user) return;
    const timeout = setTimeout(() => {
      if (activeTab === 'cursos' || activeTab === 'registrar_nota') fetchCursos();
    }, 0);
    return () => clearTimeout(timeout);
  }, [activeTab, fetchCursos, user]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  const toggleCurso = (codigo) => {
    setCursosExpandidos(prev => ({ ...prev, [codigo]: !prev[codigo] }));
  };

  // Envia una calificacion al backend y refresca la lista de cursos
  async function handleRegistrarNota(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/profesor/nota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...notaForm, calificacion: parseFloat(notaForm.calificacion) })
      });
      if (res.ok) {
        alert('Nota registrada correctamente');
        setNotaForm({ ...notaForm, identificacion_estudiante: '', calificacion: '' });
        fetchCursos();
      } else {
        const error = await res.json();
        alert('Error al registrar nota: ' + (error.detail || 'Revise los datos'));
      }
    } catch (err) { console.error(err); alert('Error de red'); }
  }

  // Calcula el promedio final de un estudiante y determina si aprobo
  const handleCerrarCurso = async (idEstudiante, codigoCurso, nombreEstudiante) => {
    if (!window.confirm(`\u00bfCerrar el curso para ${nombreEstudiante}? Se calcular\u00e1 el promedio final.`)) return;
    try {
      const res = await fetch('http://localhost:8000/api/profesor/cerrar_curso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identificacion_estudiante: idEstudiante, codigo_curso: codigoCurso })
      });
      const data = await res.json();
      if (res.ok && data.status === 'success') {
        const result = data.data;
        if (!result.tiene_notas) {
          alert('El estudiante no tiene notas registradas en este curso.');
        } else {
          alert(`Resultado de ${nombreEstudiante}:\n\nPromedio: ${result.promedio.toFixed(2)}\nEstado: ${result.aprobo ? '\u2705 Aprobado' : '\u274c Reprobado'}${result.es_nivelacion ? '\n(Curso de Nivelaci\u00f3n)' : ''}`);
        }
        fetchCursos();
      } else {
        alert(data.detail || 'Error al cerrar curso');
      }
    } catch (e) { console.error(e); alert('Error de red'); }
  };

  // Procesa el formulario de cambio de contrasena.
  // Tiene en cuenta si es un cambio obligatorio (requiere_cambio_clave) o manual.
  async function handleCambioClave(e) {
    e.preventDefault();
    if (claveForm.nueva !== claveForm.confirmacion) { alert('Las contrase\u00f1as nuevas no coinciden.'); return; }
    setCambiandoClave(true);
    try {
      let url, body;
      if (user.requiere_cambio_clave) {
        url = 'http://localhost:8000/api/cambiar_clave';
        body = { identificacion: user.id, contrasena_actual: claveForm.actual, nueva_contrasena: claveForm.nueva, confirmacion_nueva: claveForm.confirmacion, rol: 'profesor' };
      } else {
        url = `http://localhost:8000/api/profesor/${user.id}/cambiar_contrasena`;
        body = { contrasena_actual: claveForm.actual, nueva_contrasena: claveForm.nueva, confirmacion: claveForm.confirmacion };
      }
      const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const data = await res.json();
      if (res.ok) {
        alert('Contrase\u00f1a actualizada exitosamente.');
        if (user.requiere_cambio_clave) {
          const updatedUser = { ...user, requiere_cambio_clave: false };
          localStorage.setItem('user', JSON.stringify(updatedUser));
          window.location.reload();
        } else { setClaveForm({ actual: '', nueva: '', confirmacion: '' }); }
      } else { alert(data.detail || 'Error al cambiar contrase\u00f1a.'); }
    } catch (err) { console.error(err); alert('Error de red'); } finally { setCambiandoClave(false); }
  }

  if (!user) return null;

  const getColorNota = (nota) => {
    if (nota >= 7) return '#2ecc71';
    return '#e74c3c';
  };

  if (user.requiere_cambio_clave) {
    return (
      <div className="app-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div className="glass" style={{ padding: '40px', maxWidth: '400px', width: '100%' }}>
          <h2 style={{ textAlign: 'center', marginBottom: '20px', color: 'var(--primary)' }}>Cambio de Contrase\u00f1a Requerido</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '30px', textAlign: 'center', fontSize: '0.9rem' }}>Por razones de seguridad, debes cambiar tu contrase\u00f1a temporal antes de continuar.</p>
          <form onSubmit={handleCambioClave} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {['actual', 'nueva', 'confirmacion'].map((field, i) => (
              <div key={field} style={{ position: 'relative' }}>
                <input type={showPassword ? 'text' : 'password'} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} placeholder={i === 0 ? 'Contrase\u00f1a actual' : i === 1 ? 'Nueva contrase\u00f1a (m\u00ednimo 4 caracteres)' : 'Confirmar nueva contrase\u00f1a'} value={claveForm[field]} onChange={e => setClaveForm({ ...claveForm, [field]: e.target.value })} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
              </div>
            ))}
            <button type="submit" className="btn btn-primary" disabled={cambiandoClave} style={{ marginTop: '10px' }}>{cambiandoClave ? 'Actualizando...' : 'Actualizar Contrase\u00f1a'}</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">Sig<span>Ma</span></div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>PANEL PROFESOR</div>
        <nav>
          <div className={`nav-item ${activeTab === 'datos' ? 'active' : ''}`} onClick={() => setActiveTab('datos')}><User size={20} /> Ver Datos</div>
          <div className={`nav-item ${activeTab === 'cursos' ? 'active' : ''}`} onClick={() => setActiveTab('cursos')}><BookOpen size={20} /> Mis Cursos</div>
          <div className={`nav-item ${activeTab === 'registrar_nota' ? 'active' : ''}`} onClick={() => setActiveTab('registrar_nota')}><PenTool size={20} /> Registrar Nota</div>
          <div className={`nav-item ${activeTab === 'seguridad' ? 'active' : ''}`} onClick={() => setActiveTab('seguridad')}><ShieldAlert size={20} /> Seguridad</div>
        </nav>
        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" onClick={handleLogout} style={{ color: 'var(--danger)' }}><LogOut size={20} /> Cerrar Sesion</div>
        </div>
      </aside>

      <main className="main-content">
        <header style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
            {activeTab === 'datos' ? 'Mis Datos' : activeTab === 'cursos' ? 'Mis Cursos y Estudiantes' : activeTab === 'registrar_nota' ? 'Registrar Calificaci\u00f3n' : 'Seguridad'}
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Bienvenido, {user.nombre}</p>
        </header>

        {/* === VER DATOS === */}
        {activeTab === 'datos' && (
          <div className="animate-fade-in glass" style={{ padding: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(99,102,241,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}><GraduationCap size={40} /></div>
                <div>
                  <h2 style={{ fontSize: '1.8rem', margin: 0 }}>{user.nombre}</h2>
                  <p style={{ color: 'var(--text-muted)', margin: 0 }}>Profesor Titular</p>
                </div>
              </div>
              <button className="btn btn-secondary" onClick={() => setEditandoDatos(!editandoDatos)}>
                {editandoDatos ? 'Cancelar' : 'Editar Mis Datos'}
              </button>
            </div>

            {editandoDatos ? (
              <form onSubmit={handleUpdateDatos} className="dashboard-grid">
                <div className="form-group"><label>Tel\u00e9fono</label><input type="text" className="form-input" required value={datosForm.telefono} onChange={e => setDatosForm({ ...datosForm, telefono: e.target.value })} /></div>
                <div className="form-group"><label>Email</label><input type="email" className="form-input" required value={datosForm.email} onChange={e => setDatosForm({ ...datosForm, email: e.target.value })} /></div>
                <div style={{ gridColumn: 'span 2' }}><button type="submit" className="btn btn-primary" style={{ width: '100%' }}>Guardar Cambios</button></div>
              </form>
            ) : (
              <div className="dashboard-grid">
                <div className="form-group"><label>Identificaci\u00f3n</label><div className="form-input" style={{ opacity: 0.7 }}>{user.id}</div></div>
                <div className="form-group"><label>Nombre Completo</label><div className="form-input" style={{ opacity: 0.7 }}>{user.nombre}</div></div>
                <div className="form-group"><label>Tel\u00e9fono</label><div className="form-input" style={{ opacity: 0.7 }}>{user.telefono || 'No registrado'}</div></div>
                <div className="form-group"><label>Email</label><div className="form-input" style={{ opacity: 0.7 }}>{user.email || 'No registrado'}</div></div>
                <div className="form-group"><label>T\u00edtulo Acad\u00e9mico</label><div className="form-input" style={{ opacity: 0.7 }}>{user.titulo || 'No registrado'}</div></div>
                <div className="form-group"><label>Rol</label><div className="form-input" style={{ opacity: 0.7 }}>Profesor</div></div>
              </div>
            )}
          </div>
        )}

        {/* === MIS CURSOS === */}
        {activeTab === 'cursos' && (
          <div className="animate-fade-in">
            {loading ? (
              <div className="glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Cargando cursos...</div>
            ) : cursos.length === 0 ? (
              <div className="glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>No tienes cursos asignados actualmente.</div>
            ) : cursos.map(curso => (
              <div key={curso.codigo} className="glass" style={{ padding: '24px', marginBottom: '20px' }}>
                {/* Cabecera del Curso */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => toggleCurso(curso.codigo)}>
                  <div>
                    <h3 style={{ margin: 0, color: 'var(--primary)', fontSize: '1.2rem' }}>{curso.nombre}</h3>
                    <div style={{ display: 'flex', gap: '15px', marginTop: '6px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      <span style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--primary)', padding: '2px 8px', borderRadius: '4px' }}>{curso.codigo}</span>
                      {curso.creditos && <span>{curso.creditos} cr\u00e9ditos</span>}
                      {curso.semestre !== undefined && <span>Semestre {curso.semestre === 0 ? 'Nivelaci\u00f3n' : curso.semestre}</span>}
                      <span><Users size={14} style={{ display: 'inline', verticalAlign: 'middle' }} /> {curso.estudiantes?.length || 0} estudiantes</span>
                    </div>
                  </div>
                  <div>{cursosExpandidos[curso.codigo] ? <ChevronDown size={20} /> : <ChevronRight size={20} />}</div>
                </div>

                {/* Horarios y Aulas */}
                {(curso.horarios?.length > 0 || curso.aulas?.length > 0) && (
                  <div style={{ display: 'flex', gap: '20px', marginTop: '15px', flexWrap: 'wrap' }}>
                    {curso.horarios?.map((h, i) => (
                      <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(99,102,241,0.08)', padding: '6px 12px', borderRadius: '6px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                        <Calendar size={14} /> {h.dia}: {h.hora_inicio} - {h.hora_fin}
                      </div>
                    ))}
                    {curso.aulas?.map((a, i) => (
                      <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(236,72,153,0.08)', padding: '6px 12px', borderRadius: '6px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                        <MapPin size={14} /> Aula {a.numero} (Cap. {a.capacidad})
                      </div>
                    ))}
                  </div>
                )}

                {/* Lista de Estudiantes (expandible) */}
                {cursosExpandidos[curso.codigo] && (
                  <div style={{ marginTop: '20px' }}>
                    <h4 style={{ color: 'var(--text-muted)', marginBottom: '12px', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Estudiantes Matriculados</h4>
                    {curso.estudiantes?.length === 0 ? (
                      <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>No hay estudiantes matriculados en este curso.</p>
                    ) : (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        {curso.estudiantes.map(est => (
                          <div key={est.identificacion} style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '8px', padding: '16px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <div>
                                <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>{est.nombre}</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>ID: {est.identificacion} {est.email && `| ${est.email}`}</div>
                              </div>
                              <button
                                className="btn btn-secondary"
                                style={{ padding: '6px 14px', fontSize: '0.8rem', background: 'rgba(231,76,60,0.15)', borderColor: 'rgba(231,76,60,0.3)', color: '#e74c3c' }}
                                onClick={() => handleCerrarCurso(est.identificacion, curso.codigo, est.nombre)}
                              >
                                Cerrar Curso
                              </button>
                            </div>

                            {/* Evaluaciones del estudiante */}
                            {est.evaluaciones?.length > 0 ? (
                              <div style={{ marginTop: '10px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                                {est.evaluaciones.map((ev, i) => (
                                  <div key={i} style={{ background: `${getColorNota(ev.calificacion)}22`, border: `1px solid ${getColorNota(ev.calificacion)}44`, padding: '4px 10px', borderRadius: '20px', fontSize: '0.8rem', color: getColorNota(ev.calificacion) }}>
                                    {ev.nombre}: <strong>{ev.calificacion.toFixed(2)}</strong>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <div style={{ marginTop: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Sin evaluaciones registradas.</div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* === REGISTRAR NOTA === */}
        {activeTab === 'registrar_nota' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <h2 style={{ marginBottom: '20px' }}>Registrar Calificaci\u00f3n</h2>
            {cursos.length === 0 && <p style={{ color: 'var(--text-muted)', marginBottom: '15px' }}>No tienes cursos asignados. Pide al administrador que te asigne uno.</p>}
            <form onSubmit={handleRegistrarNota} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              <div className="form-group">
                <label>Curso</label>
                <select className="form-input" required value={notaForm.codigo_curso} onChange={e => setNotaForm({ ...notaForm, codigo_curso: e.target.value })}>
                  <option value="">Seleccione un curso...</option>
                  {cursos.map(c => <option key={c.codigo} value={c.codigo}>{c.nombre} ({c.codigo})</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Estudiante</label>
                <select className="form-input" required value={notaForm.identificacion_estudiante} onChange={e => setNotaForm({ ...notaForm, identificacion_estudiante: e.target.value })} disabled={!notaForm.codigo_curso}>
                  <option value="">Seleccione un estudiante...</option>
                  {(cursos.find(c => c.codigo === notaForm.codigo_curso)?.estudiantes || []).map(e => (
                    <option key={e.identificacion} value={e.identificacion}>{e.nombre} ({e.identificacion})</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Tipo de Evaluaci\u00f3n</label>
                <select className="form-input" required value={notaForm.nombre_evaluacion} onChange={e => setNotaForm({ ...notaForm, nombre_evaluacion: e.target.value })}>
                  <option value="Parcial 1">Parcial 1</option>
                  <option value="Parcial 2">Parcial 2</option>
                  <option value="Examen Final">Examen Final</option>
                  <option value="Recuperacion">Recuperaci\u00f3n</option>
                </select>
              </div>
              <div className="form-group">
                <label>Calificaci\u00f3n (0 - 10)</label>
                <input type="number" step="0.01" min="0" max="10" className="form-input" placeholder="Ej: 8.50" required value={notaForm.calificacion} onChange={e => setNotaForm({ ...notaForm, calificacion: e.target.value })} />
              </div>
              <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Calificaci\u00f3n</button>
            </form>
          </div>
        )}

        {/* === SEGURIDAD === */}
        {activeTab === 'seguridad' && (
          <div className="animate-fade-in glass" style={{ padding: '40px', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '20px' }}>Cambiar Contrase\u00f1a</h2>
            <form onSubmit={handleCambioClave} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {[['actual', 'Contrase\u00f1a actual'], ['nueva', 'Nueva contrase\u00f1a'], ['confirmacion', 'Confirmar nueva contrase\u00f1a']].map(([field, label]) => (
                <div key={field} style={{ position: 'relative' }}>
                  <label style={{ display: 'block', marginBottom: '5px', color: 'var(--text-muted)' }}>{label}</label>
                  <input type={showPassword ? 'text' : 'password'} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} value={claveForm[field]} onChange={e => setClaveForm({ ...claveForm, [field]: e.target.value })} />
                  <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
                </div>
              ))}
              <button type="submit" className="btn btn-primary" disabled={cambiandoClave} style={{ marginTop: '10px' }}>{cambiandoClave ? 'Actualizando...' : 'Guardar Nueva Contrase\u00f1a'}</button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
