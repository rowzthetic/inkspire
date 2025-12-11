import { Link } from 'react-router-dom';
import '../App.css';

export default function Signup() {
  return (
    <div className="contact" style={{ minHeight: '80vh', paddingTop: '120px' }}>
      <h2>Create an Account</h2>
      <form className="contact-form">
        <input type="text" placeholder="Full Name" required />
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit" className="btn">Sign Up</button>
      </form>
      <p style={{marginTop: '20px'}}>
        Already have an account? <Link to="/login" style={{color: '#e63946'}}>Login here</Link>
      </p>
    </div>
  );
}