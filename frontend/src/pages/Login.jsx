import { Link, useNavigate } from 'react-router-dom';
import '../App.css';

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    alert("Logged in successfully!");
    navigate('/'); // Sends user back to home
  };

  return (
    <div className="contact" style={{ minHeight: '80vh', paddingTop: '120px' }}>
      <h2>Login to Inkspire</h2>
      <form className="contact-form" onSubmit={handleLogin}>
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit" className="btn">Login</button>
      </form>
      <p style={{marginTop: '20px'}}>
        Don't have an account? <Link to="/signup" style={{color: '#e63946'}}>Sign up here</Link>
      </p>
    </div>
  );
}