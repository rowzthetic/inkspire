import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // 1. Import the Context Hook

export default function Login() {
  // We don't need useNavigate here anymore because AuthContext handles the redirect
  const { loginAction } = useAuth(); 
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setIsLoading(true);

    try {
      // 1. Perform the Fetch Request
      const response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
            throw new Error('Invalid email or password');
        }
        throw new Error(data.detail || 'Login failed');
      }

      // 2. SUCCESS: Pass the data to AuthContext
      // The context will handle localStorage, state updates, and navigation
      await loginAction(data); 

      // Optional: You can keep the alert here if you want
      // alert("Logged in successfully!");

    } catch (error) {
      console.error('Error:', error.message);
      setErrorMessage(error.message);
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="contact" style={{ minHeight: '80vh', paddingTop: '120px' }}>
      <h2>Login to Inkspire</h2>
      
      <form className="contact-form" onSubmit={handleLogin}>
        
        <input 
          type="email" 
          placeholder="Email" 
          required 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        
        <input 
          type="password" 
          placeholder="Password" 
          required 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        
        {errorMessage && (
            <div style={{
                color: '#721c24', 
                backgroundColor: '#f8d7da', 
                padding: '10px', 
                marginBottom: '15px',
                borderRadius: '4px'
            }}>
                {errorMessage}
            </div>
        )}

        <button type="submit" className="btn" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <p style={{marginTop: '20px'}}>
        Don't have an account? <Link to="/signup" style={{color: '#e63946'}}>Sign up here</Link>
      </p>
    </div>
  );
}