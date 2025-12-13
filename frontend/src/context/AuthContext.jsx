import { createContext, useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // 1. Check if user is already logged in when app loads
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        const token = localStorage.getItem('access_token');
        
        if (storedUser && token) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // 2. Global Login Function
    const loginAction = async (data) => {
        // Save to local storage
        localStorage.setItem('user', JSON.stringify({
            username: data.username,
            is_artist: data.is_artist,
            profile_image: data.profile_image
        }));
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        
        // Update State
        setUser({
            username: data.username,
            is_artist: data.is_artist,
            profile_image: data.profile_image
        });
        
        // Navigate based on role
        if (data.is_artist) {
            navigate('/artist-dashboard');
        } else {
            navigate('/');
        }
    };

    // 3. Global Logout Function
    const logoutAction = () => {
        setUser(null);
        localStorage.removeItem('user');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, loginAction, logoutAction, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

// Custom hook to use the context easily
export const useAuth = () => {
    return useContext(AuthContext);
};