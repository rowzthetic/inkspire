import { Link } from 'react-router-dom';
import '../App.css'; 

export default function Navbar() {
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
          
          {/* Added Contact Link Here */}
          <li><Link to="/contact">CONTACT</Link></li> 
          
          <li><Link to="/login" className="btn" style={{padding: '5px 15px'}}>LOGIN</Link></li>
        </ul>
      </nav>
    </header>
  );
}