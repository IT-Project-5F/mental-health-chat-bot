/**
 * Utility functions for authentication and authorization
 */

interface DecodedToken {
    sub: string;      // username
    role: string;     // user role (admin, user, etc.)
    exp: number;      // expiration timestamp
}

/**
 * Decode a JWT token without verification (client-side)
 * Note: This is for reading the payload only. Server-side validation is required for security.
 */
export function decodeToken(token: string): DecodedToken | null {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) {
            console.error('Invalid token format');
            return null;
        }

        const payload = parts[1];
        const decoded = JSON.parse(atob(payload));
        return decoded as DecodedToken;
    } catch (error) {
        console.error('Failed to decode token:', error);
        return null;
    }
}

/**
 * Get the current user's token from storage
 */
export function getToken(): string | null {
    return localStorage.getItem("access_token") || sessionStorage.getItem("access_token");
}

/**
 * Get the current user's email from storage
 */
export function getUserEmail(): string | null {
    return localStorage.getItem("user_email") || sessionStorage.getItem("user_email");
}

/**
 * Get the current user's role from the stored token
 */
export function getUserRole(): string | null {
    const token = getToken();
    if (!token) return null;

    const decoded = decodeToken(token);
    return decoded?.role || null;
}

/**
 * Check if the current user has admin role
 */
export function isAdmin(): boolean {
    const role = getUserRole();
    return role === 'admin';
}

/**
 * Check if the token is expired
 */
export function isTokenExpired(): boolean {
    const token = getToken();
    if (!token) return true;

    const decoded = decodeToken(token);
    if (!decoded) return true;

    const now = Math.floor(Date.now() / 1000);
    return decoded.exp < now;
}

/**
 * Clear authentication data
 */
export function logout(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("user_email");
    sessionStorage.removeItem("role");
    sessionStorage.removeItem("username");
}
