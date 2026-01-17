import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import './App.css';

// 1. Import Auth Context and Private Route
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Import Pages
import Home from './pages/Home';
import About from './pages/About';
import Gallery from './pages/Gallery';
import Artists from './pages/Artists';
import Shop from './pages/Shop';
import Contact from './pages/Contact';
import Explore from './pages/Explore';
import Login from './pages/Login';
import Signup from './pages/Signup';
import VerifyEmail from './pages/VerifyUserEmail';
import TattooLibrary from './pages/TattooLibrary';
import PriceEstimator from './pages/PriceEstimator';
import ArtistDashboard from './pages/ArtistDashboard';

// 👇 2. Create a Layout Helper Component
// This decides when to show/hide the Navbar & Footer
const Layout = ({ children }) => {
  const location = useLocation();
  // Check if we are on the dashboard
  const isDashboard = location.pathname === '/artist-dashboard';

  return (
    <>
      {/* Hide Navbar if on Dashboard */}
      {!isDashboard && <Navbar />}
      
      {children}
      
      {/* Hide Footer if on Dashboard */}
      {!isDashboard && <Footer />}
    </>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        {/* Wrap everything in the Layout component */}
        <Layout>
          <Routes>
            {/* --- Public Routes --- */}
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

            {/* --- Protected Routes (Login Required) --- */}
            <Route element={<PrivateRoute />}>
              <Route path="/library" element={<TattooLibrary />} />
              <Route path="/estimator" element={<PriceEstimator />} />
              
              {/* Dashboard Route */}
              <Route path="/artist-dashboard" element={<ArtistDashboard />} />
            </Route>

          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;