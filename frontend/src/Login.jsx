import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, Eye, EyeOff } from 'lucide-react';

export default function Login() {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identificacion: id, contrasena: password })
      });

      const data = await res.json();
      
      if (res.ok && data.status === 'success') {
        localStorage.setItem('user', JSON.stringify(data.data));
        
        const rol = data.data.rol;
        if (rol === 'admin') navigate('/admin');
        else if (rol === 'profesor') navigate('/profesor');
        else navigate('/estudiante');
      } else {
        setError(data.detail || 'Credenciales incorrectas');
      }
    } catch (err) {
      setError('Error al conectar con el servidor.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="glass login-card animate-fade-in">
        <div className="login-header">
          <h1>Sig<span>Ma</span></h1>
          <p>Sistema Universitario Integral</p>
        </div>
        
        <form onSubmit={handleLogin}>
          {error && <div style={{color: 'var(--danger)', marginBottom: '1rem', textAlign: 'center'}}>{error}</div>}
          
          <div className="form-group">
            <label>Identificacion</label>
            <input 
              type="text" 
              className="form-input" 
              placeholder="Ej. 0000000000"
              value={id}
              onChange={(e) => setId(e.target.value)}
              required 
            />
          </div>
          
          <div className="form-group">
            <label>Contrasena</label>
            <div style={{ position: 'relative' }}>
              <input 
                type={showPassword ? 'text' : 'password'}
                className="form-input" 
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ paddingRight: '40px' }}
                required 
              />
              <button 
                type="button" 
                onClick={() => setShowPassword(!showPassword)}
                style={{ 
                  position: 'absolute', 
                  right: '10px', 
                  top: '50%', 
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer'
                }}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>
          
          <button type="submit" className="btn btn-primary" style={{width: '100%', marginTop: '10px'}} disabled={loading}>
            {loading ? 'Verificando...' : <><LogIn size={20} /> Ingresar</>}
          </button>
        </form>
      </div>
    </div>
  );
}
