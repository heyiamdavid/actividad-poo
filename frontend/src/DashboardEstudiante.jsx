import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Library, Award, LogOut, Eye, EyeOff, BookPlus, ShieldAlert, Calendar, MapPin } from 'lucide-react';

export default function DashboardEstudiante() {
  const [activeTab, setActiveTab] = useState('datos');
  const [user] = useState(() => {
    const stored = localStorage.getItem('user');
    if (!stored) return null;
    const parsed = JSON.parse(stored);
    return parsed.rol === 'estudiante' ? parsed : null;
  });
  const navigate = useNavigate();

  const [cursos, setCursos] = useState([]);
  const [notas, setNotas] = useState([]);
  const [loadingCursos, setLoadingCursos] = useState(false);
  const [loadingNotas, setLoadingNotas] = useState(false);
  
  const [claveForm, setClaveForm] = useState({ actual: '', nueva: '', confirmacion: '' });
  const [cambiandoClave, setCambiandoClave] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [cursosDisponibles, setCursosDisponibles] = useState([]);
  const [loadingDisponibles, setLoadingDisponibles] = useState(false);
  const [selectedCursos, setSelectedCursos] = useState([]);
  const [errorMatricula, setErrorMatricula] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  const fetchCursos = useCallback(async () => {
    if (!user) return;
    setLoadingCursos(true);
    try {
      const res = await fetch(`http://localhost:8000/api/estudiante/${user.id}/cursos`);
      const data = await res.json();
      if (res.ok && data.status === 'success') setCursos(data.data);
    } catch (error) {
      console.error("Error fetching cursos", error);
    } finally {
      setLoadingCursos(false);
    }
  }, [user]);

  const fetchNotas = useCallback(async () => {
    if (!user) return;
    setLoadingNotas(true);
    try {
      const res = await fetch(`http://localhost:8000/api/estudiante/${user.id}/notas`);
      const data = await res.json();
      if (res.ok && data.status === 'success') setNotas(data.data);
    } catch (error) {
      console.error("Error fetching notas", error);
    } finally {
      setLoadingNotas(false);
    }
  }, [user]);

  const fetchCursosDisponibles = useCallback(async () => {
    if (!user) return;
    setLoadingDisponibles(true);
    setErrorMatricula('');
    try {
      const res = await fetch(`http://localhost:8000/api/estudiante/${user.id}/cursos_disponibles`);
      const data = await res.json();
      if (res.ok && data.status === 'success') {
         setCursosDisponibles(data.data);
      } else {
         setErrorMatricula(data.detail || "Error al cargar cursos disponibles");
      }
    } catch (error) {
      console.error(error);
      setErrorMatricula("Error de red");
    } finally {
      setLoadingDisponibles(false);
    }
  }, [user]);

  const handleMatricular = async () => {
    if (selectedCursos.length === 0) {
      alert("Selecciona al menos un curso");
      return;
    }
    try {
      const res = await fetch('http://localhost:8000/api/estudiante/matricular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identificacion_estudiante: user.id,
          codigos_curso: selectedCursos
        })
      });
      const data = await res.json();
      if (res.ok && data.status === 'success') {
        alert("Matrícula exitosa");
        setSelectedCursos([]);
        setActiveTab('cursos');
      } else {
        alert(data.detail || "Error en matrícula");
      }
    } catch (error) {
      console.error(error);
      alert("Error de red al matricular");
    }
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (activeTab === 'cursos') fetchCursos();
      if (activeTab === 'notas') fetchNotas();
      if (activeTab === 'matricular') fetchCursosDisponibles();
    }, 0);
    return () => clearTimeout(timeout);
  }, [activeTab, fetchCursos, fetchNotas, fetchCursosDisponibles]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  async function handleCambioClave(e) {
    e.preventDefault();
    if (claveForm.nueva !== claveForm.confirmacion) {
      alert("Las contraseñas nuevas no coinciden.");
      return;
    }
    setCambiandoClave(true);
    try {
      // Intentar primero usar la ruta especifica si no requiere forzado
      let url = 'http://localhost:8000/api/cambiar_clave';
      let body = {
        identificacion: user.id,
        contrasena_actual: claveForm.actual,
        nueva_contrasena: claveForm.nueva,
        confirmacion_nueva: claveForm.confirmacion,
        rol: 'estudiante'
      };
      
      // Si estamos en la pestaña normal de seguridad, usa la nueva ruta
      if (!user.requiere_cambio_clave) {
         url = `http://localhost:8000/api/estudiante/${user.id}/cambiar_contrasena`;
         body = {
            contrasena_actual: claveForm.actual,
            nueva_contrasena: claveForm.nueva,
            confirmacion: claveForm.confirmacion
         };
      }

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (res.ok) {
        alert("Contraseña actualizada exitosamente.");
        if (user.requiere_cambio_clave) {
            const updatedUser = { ...user, requiere_cambio_clave: false };
            localStorage.setItem('user', JSON.stringify(updatedUser));
            window.location.reload(); 
        } else {
            setClaveForm({ actual: '', nueva: '', confirmacion: '' });
        }
      } else {
        alert(data.detail || "Error al cambiar contraseña.");
      }
    } catch(err) {
      alert("Error de red");
      console.error(err);
    } finally {
      setCambiandoClave(false);
    }
  }

  if (!user) return null;

  const promedio = notas.length > 0
    ? (notas.reduce((sum, n) => sum + n.calificacion, 0) / notas.length).toFixed(2)
    : null;

  const getColorNota = (nota) => {
    if (nota >= 9) return '#2ecc71';
    if (nota >= 7) return '#f39c12';
    return '#e74c3c';
  };

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
        <div className="sidebar-header">
          Sig<span>Ma</span>
        </div>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '20px', letterSpacing: '1px' }}>
          PANEL ESTUDIANTE
        </div>

        <nav>
          <div className={`nav-item ${activeTab === 'datos' ? 'active' : ''}`} onClick={() => setActiveTab('datos')}><User size={20} /> Ver Datos</div>
          <div className={`nav-item ${activeTab === 'cursos' ? 'active' : ''}`} onClick={() => setActiveTab('cursos')}><Library size={20} /> Mis Materias</div>
          <div className={`nav-item ${activeTab === 'matricular' ? 'active' : ''}`} onClick={() => setActiveTab('matricular')}><BookPlus size={20} /> Matricularse</div>
          <div className={`nav-item ${activeTab === 'notas' ? 'active' : ''}`} onClick={() => setActiveTab('notas')}><Award size={20} /> Mis Notas</div>
          <div className={`nav-item ${activeTab === 'seguridad' ? 'active' : ''}`} onClick={() => setActiveTab('seguridad')}><ShieldAlert size={20} /> Seguridad</div>
        </nav>

        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item" onClick={handleLogout} style={{ color: 'var(--danger)' }}><LogOut size={20} /> Cerrar Sesion</div>
        </div>
      </aside>

      <main className="main-content">
        <header style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
            {activeTab === 'datos' ? 'Mi Perfil' :
             activeTab === 'cursos' ? 'Mis Materias y Horarios' : 
             activeTab === 'matricular' ? 'Matricular Cursos' :
             activeTab === 'seguridad' ? 'Seguridad y Contraseña' : 'Mis Calificaciones'}
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
               <div className="form-group"><label>Identificacion</label><div className="form-input" style={{ opacity: 0.7 }}>{user.id}</div></div>
               <div className="form-group"><label>Rol</label><div className="form-input" style={{ opacity: 0.7 }}>Estudiante</div></div>
            </div>
          </div>
        )}

        {activeTab === 'seguridad' && (
          <div className="animate-fade-in glass" style={{ padding: '40px', maxWidth: '500px' }}>
            <h2 style={{ marginBottom: '20px' }}>Cambiar Contraseña</h2>
            <form onSubmit={handleCambioClave} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ position: 'relative' }}>
                <label style={{display:'block', marginBottom:'5px', color:'var(--text-muted)'}}>Contraseña actual</label>
                <input type={showPassword ? "text" : "password"} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} value={claveForm.actual} onChange={e => setClaveForm({...claveForm, actual: e.target.value})} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
              </div>
              <div style={{ position: 'relative' }}>
                <label style={{display:'block', marginBottom:'5px', color:'var(--text-muted)'}}>Nueva contraseña</label>
                <input type={showPassword ? "text" : "password"} required minLength="4" className="form-input" style={{ width: '100%', paddingRight: '40px' }} value={claveForm.nueva} onChange={e => setClaveForm({...claveForm, nueva: e.target.value})} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
              </div>
              <div style={{ position: 'relative' }}>
                <label style={{display:'block', marginBottom:'5px', color:'var(--text-muted)'}}>Confirmar nueva contraseña</label>
                <input type={showPassword ? "text" : "password"} required className="form-input" style={{ width: '100%', paddingRight: '40px' }} value={claveForm.confirmacion} onChange={e => setClaveForm({...claveForm, confirmacion: e.target.value})} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '35px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
              </div>
              <button type="submit" className="btn btn-primary" disabled={cambiandoClave} style={{ marginTop: '10px' }}>{cambiandoClave ? 'Actualizando...' : 'Guardar Nueva Contraseña'}</button>
            </form>
          </div>
        )}

        {activeTab === 'cursos' && (
          <div className="animate-fade-in">
            {loadingCursos ? (
              <div className="glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Cargando materias...</div>
            ) : cursos.length === 0 ? (
              <div className="glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>No tienes materias matriculadas actualmente.</div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }}>
                {cursos.map(c => (
                  <div key={c.codigo} className="glass" style={{ padding: '24px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                      <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{c.nombre}</h3>
                      <span style={{ background: 'rgba(99,102,241,0.2)', color: 'var(--primary)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', whiteSpace: 'nowrap' }}>{c.codigo}</span>
                    </div>
                    <div style={{ display: 'flex', gap: '15px', color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '15px' }}>
                      <span>Semestre {c.semestre}</span>
                      <span>{c.creditos} créditos</span>
                    </div>
                    
                    {c.horarios && c.horarios.length > 0 && (
                      <div style={{ background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '6px' }}>
                        <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--text)' }}>Horarios:</h4>
                        {c.horarios.map((h, i) => (
                           <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '5px' }}>
                             <Calendar size={14} /> {h.dia}: {h.hora_inicio} - {h.hora_fin}
                           </div>
                        ))}
                      </div>
                    )}

                    {c.aulas && c.aulas.length > 0 && (
                      <div style={{ background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '6px', marginTop: '10px' }}>
                        <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--text)' }}>Aulas:</h4>
                        {c.aulas.map((a, i) => (
                           <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '5px' }}>
                             <MapPin size={14} /> Aula {a.numero} (Capacidad: {a.capacidad})
                           </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'matricular' && (
          <div className="animate-fade-in glass" style={{ padding: '24px' }}>
            <h2 style={{ marginBottom: '20px' }}>Selección de Cursos</h2>
            {errorMatricula && <div style={{ background: 'rgba(231,76,60,0.1)', color: 'var(--danger)', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>{errorMatricula}</div>}
            {loadingDisponibles ? <p style={{ color: 'var(--text-muted)', textAlign: 'center' }}>Cargando materias disponibles...</p> : cursosDisponibles.length === 0 ? <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>{!errorMatricula && "No hay materias disponibles para tu carrera y semestre en este momento."}</p> : (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px', marginBottom: '20px' }}>
                  {cursosDisponibles.map(c => {
                    const isSelected = selectedCursos.includes(c.codigo);
                    return (
                      <div key={c.codigo} onClick={() => { if (isSelected) setSelectedCursos(selectedCursos.filter(code => code !== c.codigo)); else setSelectedCursos([...selectedCursos, c.codigo]); }} className="glass" style={{ padding: '24px', cursor: 'pointer', border: isSelected ? '2px solid var(--primary)' : '2px solid transparent', transition: 'all 0.2s ease' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                          <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{c.nombre}</h3>
                          <span style={{ background: 'rgba(99,102,241,0.2)', color: 'var(--primary)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', whiteSpace: 'nowrap' }}>{c.codigo}</span>
                        </div>
                        <div style={{ display: 'flex', gap: '15px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                          <span>Semestre {c.semestre}</span>
                          <span>{c.creditos} créditos</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
                <button onClick={handleMatricular} className="btn btn-primary" style={{ width: '100%' }}>Confirmar Matrícula ({selectedCursos.length} cursos seleccionados)</button>
              </>
            )}
          </div>
        )}

        {activeTab === 'notas' && (
          <div className="animate-fade-in">
            {promedio && (
              <div className="dashboard-grid" style={{ marginBottom: '20px' }}>
                <div className="glass stat-card">
                  <div className="stat-icon"><Award size={24} /></div>
                  <div className="stat-info"><h3 style={{ color: getColorNota(parseFloat(promedio)) }}>{promedio}</h3><p>Promedio General</p></div>
                </div>
              </div>
            )}

            <div className="glass" style={{ padding: '24px' }}>
              <h2 style={{ marginBottom: '20px' }}>Historial de Calificaciones</h2>
              {loadingNotas ? <p style={{ color: 'var(--text-muted)', textAlign: 'center' }}>Cargando notas...</p> : notas.length === 0 ? <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>Aún no tienes calificaciones registradas.</p> : (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead><tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}><th style={{ padding: '12px', color: 'var(--text-muted)' }}>Curso</th><th style={{ padding: '12px', color: 'var(--text-muted)' }}>Evaluación</th><th style={{ padding: '12px', color: 'var(--text-muted)' }}>Nota</th></tr></thead>
                  <tbody>
                    {notas.map((n, i) => (
                      <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                        <td style={{ padding: '12px' }}>{n.codigo_curso}</td>
                        <td style={{ padding: '12px' }}>{n.evaluacion}</td>
                        <td style={{ padding: '12px' }}><span style={{ padding: '4px 12px', borderRadius: '20px', fontWeight: 'bold', fontSize: '0.9rem', backgroundColor: `${getColorNota(n.calificacion)}22`, color: getColorNota(n.calificacion) }}>{n.calificacion.toFixed(2)}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
