import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
    children: React.ReactNode
    requiredRole?: string
}

function ProtectedRoute( { children, requiredRole }: ProtectedRouteProps) {
    const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");
    const role = localStorage.getItem("role") || sessionStorage.getItem("role");

    if (!token) {
        return <Navigate to="/login" replace />
    }

    if (requiredRole && role !== requiredRole) {
        return <Navigate to="/" replace />
    }

    return <>{children}</>
}

export default ProtectedRoute;