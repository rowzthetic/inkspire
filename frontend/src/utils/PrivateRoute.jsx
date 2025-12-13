import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = () => {
    const { user } = useAuth();

    // If user is not logged in, redirect to login page
    if (!user) return <Navigate to="/login" />;

    // If logged in, render the child routes
    return <Outlet />;
};

export default PrivateRoute;