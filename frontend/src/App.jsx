import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Explore from './pages/Explore';

// Import Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Import Pages
import Home from './pages/Home';
import About from './pages/About';
import Gallery from './pages/Gallery';
import Artists from './pages/Artists';
import Shop from './pages/Shop';
import Contact from './pages/Contact';
import PriceEstimator from './pages/PriceEstimator';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <Router>
      <Navbar />
      
      {/* This section switches the content based on the URL */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/gallery" element={<Gallery />} />
        <Route path="/artists" element={<Artists />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/estimator" element={<PriceEstimator />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/explore" element={<Explore />} />
      </Routes>

      <Footer />
    </Router>
  );
}

export default App;