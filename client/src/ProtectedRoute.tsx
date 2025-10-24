import { Navigate } from "react-router-dom";
import { getToken, isTokenExpired, getUserRole } from "./utils/auth";

interface ProtectedRouteProps {
    children: React.ReactNode;
    requireAdmin?: boolean;  // Optional prop to require admin role
}

function ProtectedRoute({ children, requireAdmin = false }: ProtectedRouteProps) {
    const token = getToken();

    // Check if token exists
    if (!token) {
        return <Navigate to="/login" replace />
    }

    // Check if token is expired
    if (isTokenExpired()) {
        // Clear expired token
        localStorage.removeItem("access_token");
        sessionStorage.removeItem("access_token");
        return <Navigate to="/login" replace />
    }

    // Check admin role if required
    if (requireAdmin) {
        const role = getUserRole();
        if (role !== "admin") {
            // Redirect non-admin users to home page
            return <Navigate to="/" replace />
        }
    }

    return <>{children}</>
}

export default ProtectedRoute;