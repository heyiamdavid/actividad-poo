import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import DashboardAdmin from './DashboardAdmin';
import DashboardProfesor from './DashboardProfesor';
import DashboardEstudiante from './DashboardEstudiante';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/admin" element={<DashboardAdmin />} />
        <Route path="/profesor" element={<DashboardProfesor />} />
        <Route path="/estudiante" element={<DashboardEstudiante />} />
      </Routes>
    </BrowserRouter>
  );
}
