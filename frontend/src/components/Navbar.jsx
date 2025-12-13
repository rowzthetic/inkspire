import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; 
import '../App.css'; 

export default function Navbar() {
  const { user, logoutAction } = useAuth();

  return (
    <header className="navbar">
      <div className="logo">INKSPIRE</div>
      <nav>
        <ul className="nav-links">
          <li><Link to="/">HOME</Link></li>
          <li><Link to="/about">ABOUT</Link></li>
          <li><Link to="/gallery">GALLERY</Link></li>
          <li><Link to="/artists">ARTISTS</Link></li>
          <li><Link to="/shop">OUR SHOP</Link></li>
          <li><Link to="/explore">EXPLORE</Link></li>
          <li><Link to="/contact">CONTACT</Link></li>
          
          {!user ? (
            <>
              <li>
                <Link to="/login" className="btn" style={{padding: '5px 15px', marginRight: '10px'}}>
                  LOGIN
                </Link>
              </li>
              <li>
                <Link to="/signup" style={{fontWeight: 'bold'}}>SIGNUP</Link>
              </li>
            </>
          ) : (
            <>
              <li style={{ color: '#e63946', fontWeight: 'bold' }}>
                Hello, {user.username || 'User'}
              </li>
              <li>
                <button 
                  onClick={logoutAction} 
                  className="btn" 
                  style={{
                    padding: '5px 15px', 
                    cursor: 'pointer', 
                    background: 'transparent', 
                    border: '1px solid currentColor'
                  }}
                >
                  LOGOUT
                </button>
              </li>
            </>
          )}

        </ul>
      </nav>
    </header>
  );
}