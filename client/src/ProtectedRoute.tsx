import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

function ProtectedRoute( { children }: ProtectedRouteProps) {
    const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");

    if (!token) {
        return <Navigate to="/login" replace/>
    }

    return <>{children}</>
}

export default ProtectedRoute;