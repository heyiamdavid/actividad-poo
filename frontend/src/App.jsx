import { useState } from 'react';

const STEPS = [
  { id: 1, label: 'Régimen' },
  { id: 2, label: 'Estudiante' },
  { id: 3, label: 'Profesor'},
  { id: 4, label: 'Curso'},
  { id: 5, label: 'Logística'},
  { id: 6, label: 'Confirmar'},
];

const INITIAL = {
  opcion_regimen: '1',
  estudiante: { nombre: '', telefono: '', email: '', id: '', contra: '', prom_ingreso: 0, prom_graduacion: 0, estado: 'Activo', modalidad: 'Presencial' },
  profesor:    { nombre: '', telefono: '', email: '', id: '', contra: '', materia: '', titulo: '' },
  curso:       { nombre: '', paralelo: 'A', codigo: '', creditos: '' },
  horario:     { dia: 'Lunes', horaInicio: '08:00', horaFin: '10:00' },
  aula:        { numero: '', capacidad: 30 },
  evaluacion:  { nombre: 'Parcial 1', nota: 10 },
  fecha_matricula: new Date().toISOString().split('T')[0],
};

export default function App() {
  const [step, setStep]       = useState(1);
  const [done, setDone]       = useState([]);
  const [formData, setForm]   = useState(INITIAL);
  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState(null);

  const set = (section, field, value) => {
    if (section === 'root') {
      setForm(f => ({ ...f, [field]: value }));
    } else {
      setForm(f => ({ ...f, [section]: { ...f[section], [field]: value } }));
    }
  };

  const advance = () => {
    setDone(d => d.includes(step) ? d : [...d, step]);
    setStep(s => Math.min(s + 1, 6));
  };

  const goTo = (s) => { if (s < step || done.includes(s - 1) || s === 1) setStep(s); };

  const submit = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res  = await fetch('http://localhost:8000/api/matricular', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.status === 'success') {
        setResult(data.data);
        setDone(STEPS.map(s => s.id));
      } else {
        alert('Error en el servidor. Revisa la consola del backend.');
      }
    } catch {
      alert('No se pudo conectar. ¿Está corriendo el backend? (python -m uvicorn api:app --reload)');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="layout">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-logo">Sig<span>Ma</span></div>
        {STEPS.map(s => (
          <div
            key={s.id}
            className={`step-item ${step === s.id ? 'active' : ''} ${done.includes(s.id) ? 'done' : ''}`}
            onClick={() => goTo(s.id)}
          >
            <div className="step-num">
              {done.includes(s.id) ? '✓' : s.id}
            </div>
            <span>{s.icon} {s.label}</span>
          </div>
        ))}
      </aside>

      {/* MAIN */}
      <main className="main">
        <div className="page-header">
          <h1>Registro de Matrícula</h1>
          <p>Paso {step} de 6 — {STEPS[step - 1].label}</p>
        </div>

        {/* STEP 1 — Régimen */}
        {step === 1 && (
          <div className="card">
            <div className="card-header">
              
              <h2>Seleccione el Régimen Académico</h2>
            </div>
            <div className="regimen-toggle">
              <div
                className={`regimen-option ${formData.opcion_regimen === '1' ? 'selected' : ''}`}
                onClick={() => set('root', 'opcion_regimen', '1')}
              >
                <div className="ro-title">Régimen Regular</div>
                <div className="ro-desc">Para estudiantes en carreras con créditos y código de materia.</div>
              </div>
              <div
                className={`regimen-option ${formData.opcion_regimen === '2' ? 'selected' : ''}`}
                onClick={() => set('root', 'opcion_regimen', '2')}
              >
                <div className="ro-title">Régimen de Nivelación</div>
                <div className="ro-desc">Para estudiantes en proceso de nivelación con paralelos.</div>
              </div>
            </div>
            <div className="actions" style={{ marginTop: '1.5rem' }}>
              <button className="btn-primary" onClick={advance}>Siguiente →</button>
            </div>
          </div>
        )}

        {/* STEP 2 — Estudiante */}
        {step === 2 && (
          <div className="card">
            <div className="card-header">
              <h2>Información del Estudiante</h2>
            </div>
            <div className="grid-2">
              <div className="form-group">
                <label>Nombre Completo</label>
                <input type="text" placeholder="Ej. Juan Pérez" value={formData.estudiante.nombre} onChange={e => set('estudiante', 'nombre', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Identificación (Cédula)</label>
                <input type="text" placeholder="0912345678" value={formData.estudiante.id} onChange={e => set('estudiante', 'id', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Correo Electrónico</label>
                <input type="email" placeholder="correo@universidad.edu" value={formData.estudiante.email} onChange={e => set('estudiante', 'email', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Teléfono</label>
                <input type="tel" placeholder="0991234567" value={formData.estudiante.telefono} onChange={e => set('estudiante', 'telefono', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Promedio de Ingreso</label>
                <input type="number" step="0.1" min="0" max="10" value={formData.estudiante.prom_ingreso} onChange={e => set('estudiante', 'prom_ingreso', parseFloat(e.target.value))} />
              </div>
              <div className="form-group">
                <label>Modalidad</label>
                <select value={formData.estudiante.modalidad} onChange={e => set('estudiante', 'modalidad', e.target.value)}>
                  <option>Presencial</option>
                  <option>Virtual</option>
                  <option>Semipresencial</option>
                </select>
              </div>
            </div>
            <div className="actions">
              <button className="btn-secondary" onClick={() => setStep(1)}>← Atrás</button>
              <button className="btn-primary" onClick={advance}>Siguiente →</button>
            </div>
          </div>
        )}

        {/* STEP 3 — Profesor */}
        {step === 3 && (
          <div className="card">
            <div className="card-header">
              <h2>Información del Profesor</h2>
            </div>
            <div className="grid-2">
              <div className="form-group">
                <label>Nombre del Profesor</label>
                <input type="text" placeholder="Ej. Dra. Ana Gómez" value={formData.profesor.nombre} onChange={e => set('profesor', 'nombre', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Materia a Impartir</label>
                <input type="text" placeholder="Ej. Matemáticas" value={formData.profesor.materia} onChange={e => set('profesor', 'materia', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Título Académico</label>
                <input type="text" placeholder="Ej. PhD en Ciencias" value={formData.profesor.titulo} onChange={e => set('profesor', 'titulo', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Correo Electrónico</label>
                <input type="email" placeholder="profesor@universidad.edu" value={formData.profesor.email} onChange={e => set('profesor', 'email', e.target.value)} />
              </div>
            </div>
            <div className="actions">
              <button className="btn-secondary" onClick={() => setStep(2)}>← Atrás</button>
              <button className="btn-primary" onClick={advance}>Siguiente →</button>
            </div>
          </div>
        )}

        {/* STEP 4 — Curso */}
        {step === 4 && (
          <div className="card">
            <div className="card-header">
              <h2>Detalles del Curso</h2>
            </div>
            <div className="grid-2">
              <div className="form-group">
                <label>Nombre del Curso</label>
                <input type="text" placeholder="Ej. Álgebra Lineal" value={formData.curso.nombre} onChange={e => set('curso', 'nombre', e.target.value)} />
              </div>
              {formData.opcion_regimen === '2' ? (
                <div className="form-group">
                  <label>Paralelo</label>
                  <input type="text" placeholder="Ej. A" value={formData.curso.paralelo} onChange={e => set('curso', 'paralelo', e.target.value)} />
                </div>
              ) : (
                <>
                  <div className="form-group">
                    <label>Código del Curso</label>
                    <input type="text" placeholder="Ej. MAT-101" value={formData.curso.codigo} onChange={e => set('curso', 'codigo', e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label>Créditos</label>
                    <input type="number" placeholder="Ej. 3" value={formData.curso.creditos} onChange={e => set('curso', 'creditos', e.target.value)} />
                  </div>
                </>
              )}
              <div className="form-group">
                <label>Fecha de Matrícula</label>
                <input type="date" value={formData.fecha_matricula} onChange={e => set('root', 'fecha_matricula', e.target.value)} />
              </div>
            </div>
            <div className="actions">
              <button className="btn-secondary" onClick={() => setStep(3)}>← Atrás</button>
              <button className="btn-primary" onClick={advance}>Siguiente →</button>
            </div>
          </div>
        )}

        {/* STEP 5 — Logística */}
        {step === 5 && (
          <div className="card">
            <div className="card-header">
              <h2>Horario y Aula</h2>
            </div>
            <div className="grid-3">
              <div className="form-group">
                <label>Día</label>
                <select value={formData.horario.dia} onChange={e => set('horario', 'dia', e.target.value)}>
                  {['Lunes','Martes','Miércoles','Jueves','Viernes'].map(d => <option key={d}>{d}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Hora Inicio</label>
                <input type="time" value={formData.horario.horaInicio} onChange={e => set('horario', 'horaInicio', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Hora Fin</label>
                <input type="time" value={formData.horario.horaFin} onChange={e => set('horario', 'horaFin', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Número de Aula</label>
                <input type="text" placeholder="Ej. B-201" value={formData.aula.numero} onChange={e => set('aula', 'numero', e.target.value)} />
              </div>
              <div className="form-group">
                <label>Capacidad</label>
                <input type="number" value={formData.aula.capacidad} onChange={e => set('aula', 'capacidad', parseInt(e.target.value))} />
              </div>
            </div>
            <div className="actions">
              <button className="btn-secondary" onClick={() => setStep(4)}>← Atrás</button>
              <button className="btn-primary" onClick={advance}>Revisar →</button>
            </div>
          </div>
        )}

        {/* STEP 6 — Confirmar */}
        {step === 6 && !result && (
          <div className="card">
            <div className="card-header">
              <h2>Resumen y Confirmación</h2>
            </div>
            <div className="result-grid">
              <div className="result-item">
                <div className="result-label">Régimen</div>
                <div className="result-value">{formData.opcion_regimen === '1' ? 'Regular' : 'Nivelación'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Estudiante</div>
                <div className="result-value">{formData.estudiante.nombre || '—'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Profesor</div>
                <div className="result-value">{formData.profesor.nombre || '—'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Curso</div>
                <div className="result-value">{formData.curso.nombre || '—'}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Horario</div>
                <div className="result-value">{formData.horario.dia} · {formData.horario.horaInicio}–{formData.horario.horaFin}</div>
              </div>
              <div className="result-item">
                <div className="result-label">Aula</div>
                <div className="result-value">{formData.aula.numero || '—'}</div>
              </div>
            </div>
            <div className="actions">
              <button className="btn-secondary" onClick={() => setStep(5)}>← Editar</button>
              <button className="btn-primary" onClick={submit} disabled={loading}>
                {loading ? 'Guardando...' : ' Confirmar Matrícula'}
              </button>
            </div>
          </div>
        )}

        {/* SUCCESS */}
        {result && (
          <div className="success-banner">
            <div>
              <div className="success-title">¡Matrícula Registrada Exitosamente!</div>
              <div className="success-body">
                Guardada con ID #{result.matricula?.id} · {result.estudiante?.nombre} → {result.curso?.nombre}
              </div>
              <div className="result-grid" style={{marginTop: '1rem'}}>
                {Object.entries(result).map(([key, val]) => (
                  <div className="result-item" key={key}>
                    <div className="result-label">{key}</div>
                    <div className="result-value">{typeof val === 'object' ? Object.values(val).join(' · ') : val}</div>
                  </div>
                ))}
              </div>
              <button className="btn-secondary" style={{marginTop: '1rem'}} onClick={() => { setForm(INITIAL); setStep(1); setDone([]); setResult(null); }}>
                + Nueva Matrícula
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
