import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// 1. Import Auth Context and Private Route
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';

import Explore from './pages/Explore';
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
import VerifyEmail from './pages/VerifyUserEmail';
import TattooLibrary from './pages/TattooLibrary';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/artists" element={<Artists />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/activate/:uid/:token" element={<VerifyEmail />} />
          <Route path="/activate/:token" element={<VerifyEmail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/estimator" element={<PriceEstimator />} />
          <Route element={<PrivateRoute />}>
          <Route path="/library" element={<TattooLibrary />} />
             {/* <Route path="/estimator" element={<PriceEstimator />} /> */}
          </Route>

        </Routes>

        <Footer />
      </AuthProvider>
    </Router>
  );
}

export default App;