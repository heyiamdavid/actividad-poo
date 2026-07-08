import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, PenTool, ListChecks, LogOut, GraduationCap, Eye, EyeOff } from 'lucide-react';

export default function DashboardProfesor() {
  const [activeTab, setActiveTab] = useState('datos');
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    if (!stored) return null;
    const parsed = JSON.parse(stored);
    return parsed.rol === 'profesor' ? parsed : null;
  });
  const navigate = useNavigate();
  
  const [cursos, setCursos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notaForm, setNotaForm] = useState({ identificacion_estudiante: '', codigo_curso: '', nombre_evaluacion: 'Parcial 1', calificacion: '' });
  const [claveForm, setClaveForm] = useState({ actual: '', nueva: '', confirmacion: '' });
  const [cambiandoClave, setCambiandoClave] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  const [editandoDatos, setEditandoDatos] = useState(false);
  const [datosForm, setDatosForm] = useState({ telefono: user?.telefono || '', email: user?.email || '' });

  const handleUpdateDatos = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:8000/api/profesor/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosForm)
      });
      if (res.ok) {
        alert("Datos actualizados");
        const updatedUser = { ...user, ...datosForm };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        window.location.reload();
      } else {
        alert("Error al actualizar datos");
      }
    } catch(err) { alert("Error de red"); }
  };

  const handleCerrarCurso = async (idEstudiante, codigoCurso) => {
    if (!window.confirm("¿Seguro que deseas cerrar el curso para este estudiante? Se calculará el promedio final y su estado.")) return;
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
          alert("El estudiante no tiene notas registradas en este curso.");
        } else {
          alert(`Promedio: ${result.promedio.toFixed(2)}\nEstado: ${result.aprobo ? 'Aprobado' : 'Reprobado'}\n${result.es_nivelacion ? '(Curso de Nivelación)' : ''}`);
        }
      } else {
        alert(data.detail || "Error al cerrar curso");
      }
    } catch(err) {
      alert("Error de red");
    }
  };

  const fetchCursos = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/profesor/${user.id}/cursos`);
      const data = await res.json();
      if (res.ok && data.status === 'success') setCursos(data.data);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  }, [user]);

  useEffect(() => {
    if (!user) {
      navigate('/login');
    } else {
      if (activeTab === 'ver_evaluaciones' || activeTab === 'registrar_nota') {
        fetchCursos();
      }
    }
  }, [user, navigate, activeTab, fetchCursos]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  async function handleRegistrarNota(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/profesor/nota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...notaForm,
          calificacion: parseFloat(notaForm.calificacion)
        })
      });
      if (res.ok) {
        alert("Nota registrada correctamente");
        setNotaForm({...notaForm, identificacion_estudiante: '', calificacion: ''});
      } else {
        const error = await res.json();
        alert("Error al registrar nota: " + (error.detail || "Revise los datos"));
      }
    } catch(err) { 
      console.error(err);
      alert("Error de red"); 
    }
  }

  async function handleCambioClave(e) {
    e.preventDefault();
    if (claveForm.nueva !== claveForm.confirmacion) {
      alert("Las contraseñas nuevas no coinciden.");
      return;
    }
    setCambiandoClave(true);
    try {
      const res = await fetch('http://localhost:8000/api/cambiar_clave', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identificacion: user.id,
          contrasena_actual: claveForm.actual,
          nueva_contrasena: claveForm.nueva,
          confirmacion_nueva: claveForm.confirmacion,
          rol: 'profesor'
        })
      });
      const data = await res.json();
      if (res.ok) {
        alert("Contraseña actualizada exitosamente.");
        const updatedUser = { ...user, requiere_cambio_clave: false };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        window.location.reload();
      } else {
        alert(data.detail || "Error al cambiar contraseña.");
      }
    } catch(err) {
      console.error(err);
      alert("Error de red");
    } finally {
      setCambiandoClave(false);
    }
  }

  if (!user) return null;

  if (user.requiere_cambio_clave) {
    return (
      <div className="app-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div className="glass" style={{ padding: '40px', maxWidth: '400px', width: '100%' }}>
          <h2 style={{ textAlign: 'center', marginBottom: '20px', color: 'var(--primary)' }}>Cambio de Contraseña Requerido</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '30px', textAlign: 'center', fontSize: '0.9rem' }}>
            Por razones de seguridad, debes cambiar tu contraseña temporal antes de continuar.
          </p>
          <form onSubmit={handleCambioClave} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <div style={{ position: 'relative' }}>
              <input type={showPassword ? "text" : "password"} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} placeholder="Contraseña actual" value={claveForm.actual} onChange={e => setClaveForm({...claveForm, actual: e.target.value})} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            <div style={{ position: 'relative' }}>
              <input type={showPassword ? "text" : "password"} required minLength="4" className="form-input" style={{ width: '100%', paddingRight: '40px' }} placeholder="Nueva contraseña (mínimo 4 caracteres)" value={claveForm.nueva} onChange={e => setClaveForm({...claveForm, nueva: e.target.value})} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            <div style={{ position: 'relative' }}>
              <input type={showPassword ? "text" : "password"} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} placeholder="Confirmar nueva contraseña" value={claveForm.confirmacion} onChange={e => setClaveForm({...claveForm, confirmacion: e.target.value})} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            <button type="submit" className="btn btn-primary" disabled={cambiandoClave} style={{ marginTop: '10px' }}>
              {cambiandoClave ? 'Actualizando...' : 'Actualizar Contraseña'}
            </button>
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
          <div className={`nav-item ${activeTab === 'registrar_nota' ? 'active' : ''}`} onClick={() => setActiveTab('registrar_nota')}><PenTool size={20} /> Registrar Nota</div>
          <div className={`nav-item ${activeTab === 'ver_evaluaciones' ? 'active' : ''}`} onClick={() => setActiveTab('ver_evaluaciones')}><ListChecks size={20} /> Mis Cursos</div>
        </nav>
        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" onClick={handleLogout} style={{ color: 'var(--danger)' }}><LogOut size={20} /> Cerrar Sesion</div>
        </div>
      </aside>

      <main className="main-content">
        <header style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>{activeTab === 'datos' ? 'Mis Datos' : activeTab === 'registrar_nota' ? 'Calificar Alumnos' : 'Mis Cursos y Estudiantes'}</h1>
          <p style={{ color: 'var(--text-muted)' }}>Bienvenido, {user.nombre}</p>
        </header>

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
                <div className="form-group">
                  <label>Teléfono</label>
                  <input type="text" className="form-input" required value={datosForm.telefono} onChange={e => setDatosForm({...datosForm, telefono: e.target.value})} />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" className="form-input" required value={datosForm.email} onChange={e => setDatosForm({...datosForm, email: e.target.value})} />
                </div>
                <div style={{ gridColumn: 'span 2' }}>
                  <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>Guardar Cambios</button>
                </div>
              </form>
            ) : (
              <div className="dashboard-grid">
                 <div className="form-group">
                   <label>Identificación</label>
                   <div className="form-input" style={{ opacity: 0.7 }}>{user.id}</div>
                 </div>
                 <div className="form-group">
                   <label>Teléfono</label>
                   <div className="form-input" style={{ opacity: 0.7 }}>{user.telefono || 'No registrado'}</div>
                 </div>
                 <div className="form-group">
                   <label>Email</label>
                   <div className="form-input" style={{ opacity: 0.7 }}>{user.email || 'No registrado'}</div>
                 </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'registrar_nota' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <h2>Registrar Calificación</h2>
            <form onSubmit={handleRegistrarNota} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginTop: '20px' }}>
              
              <div className="form-group">
                <label>Seleccionar Curso</label>
                <select className="form-input" required value={notaForm.codigo_curso} onChange={e => setNotaForm({...notaForm, codigo_curso: e.target.value})}>
                  <option value="">Seleccione un curso...</option>
                  {cursos.map(c => <option key={c.codigo} value={c.codigo}>{c.nombre} ({c.codigo})</option>)}
                </select>
              </div>

              <div className="form-group">
                <label>Evaluación</label>
                <select className="form-input" required value={notaForm.nombre_evaluacion} onChange={e => setNotaForm({...notaForm, nombre_evaluacion: e.target.value})}>
                  <option value="Parcial 1">Parcial 1</option>
                  <option value="Parcial 2">Parcial 2</option>
                  <option value="Examen Final">Examen Final</option>
                  <option value="Recuperacion">Recuperación</option>
                </select>
              </div>

              <div className="form-group">
                <label>Identificación Estudiante</label>
                <input type="text" className="form-input" placeholder="ID del estudiante" required value={notaForm.identificacion_estudiante} onChange={e => setNotaForm({...notaForm, identificacion_estudiante: e.target.value})} />
              </div>

              <div className="form-group">
                <label>Calificación</label>
                <input type="number" step="0.01" min="0" max="10" className="form-input" placeholder="0.00 - 10.00" required value={notaForm.calificacion} onChange={e => setNotaForm({...notaForm, calificacion: e.target.value})} />
              </div>

              <button type="submit" className="btn btn-primary" style={{ gridColumn: 'span 2' }}>Guardar Calificación</button>
            </form>
          </div>
        )}

        {activeTab === 'ver_evaluaciones' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <h2>Mis Cursos Asignados</h2>
            {loading ? <p>Cargando cursos...</p> : (
              <div>
                {cursos.map(curso => (
                  <div key={curso.codigo} style={{ marginBottom: '30px', background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '8px' }}>
                    <h3 style={{ color: 'var(--primary)', marginBottom: '15px' }}>{curso.nombre} ({curso.codigo})</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                      <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th>ID Estudiante</th><th>Nombre</th><th style={{ textAlign: 'right' }}>Acción</th></tr></thead>
                      <tbody>
                        {curso.estudiantes && curso.estudiantes.length > 0 ? curso.estudiantes.map(e => (
                          <tr key={e.identificacion} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                            <td style={{ padding: '12px' }}>{e.identificacion}</td>
                            <td style={{ padding: '12px' }}>{e.nombre}</td>
                            <td style={{ padding: '12px', textAlign: 'right' }}>
                              <button className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => handleCerrarCurso(e.identificacion, curso.codigo)}>
                                Cerrar Curso
                              </button>
                            </td>
                          </tr>
                        )) : <tr><td colSpan="3" style={{ padding: '12px', color: 'var(--text-muted)' }}>No hay estudiantes matriculados</td></tr>}
                      </tbody>
                    </table>
                  </div>
                ))}
                {cursos.length === 0 && <p style={{ color: 'var(--text-muted)' }}>No tienes cursos asignados.</p>}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
