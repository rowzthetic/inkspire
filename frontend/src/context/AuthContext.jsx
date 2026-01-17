import { createContext, useState, useEffect, useContext } from 'react';
// ❌ Remove useNavigate import
// import { useNavigate } from 'react-router-dom'; 

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    // ❌ Remove navigate hook
    // const navigate = useNavigate();

    // 1. Check if user is already logged in when app loads
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        const token = localStorage.getItem('access'); // Ensure this matches what you save below ('access' or 'access_token')
        
        if (storedUser && token) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // 2. Global Login Function (PURE DATA ONLY)
    const loginAction = async (data) => {
        // Save to local storage
        localStorage.setItem('user', JSON.stringify({
            username: data.username,
            is_artist: data.is_artist,
            profile_image: data.profile_picture // Ensure this matches backend key
        }));
        
        // Consistency is key: use 'access' if that's what Django sends
        localStorage.setItem('access', data.access); 
        localStorage.setItem('refresh', data.refresh);
        
        // Update State
        setUser({
            username: data.username,
            is_artist: data.is_artist,
            profile_image: data.profile_picture
        });
        
        // ❌ DELETE ALL NAVIGATION LOGIC FROM HERE
        // Login.jsx will handle the redirect!
    };

    // 3. Global Logout Function
    const logOut = () => {
        setUser(null);
        localStorage.removeItem('user');
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        
        // Hard redirect is safer for logout to clear memory
        window.location.href = '/login'; 
    };

    return (
        <AuthContext.Provider value={{ user, loginAction, logOut, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};