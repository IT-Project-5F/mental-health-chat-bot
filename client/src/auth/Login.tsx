import { useNavigate, Link } from 'react-router-dom';
import { useState } from 'react';
import { request } from '@/api';
import { Button } from '@/components/ui/button';
import PasswordResetModal from './PasswordResetModal';

/**
 * Description:
 * - Login page collects username and password to determine
 */
function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [remember, setRemember] = useState(false);
    const [resetModal, setResetModal] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const result = await request("POST", "/api/auth/login", { username, password }, true, "form");

            if (result && result.access_token) {
                // Check if user selected "Remember"
                if (remember) {
                    // Persist login
                    localStorage.setItem("access_token", result.access_token);
                    localStorage.setItem("username", result.username);
                    localStorage.setItem("email", result.email_address);
                } else {
                    // Clears (signs out) when browser closes
                    sessionStorage.setItem("access_token", result.access_token);
                    sessionStorage.setItem("username", result.username);
                    sessionStorage.setItem("email", result.email_address);
                }
                if (result.role == "admin") {
                    navigate('/admin');
                } else {
                    alert("Login success");
                    navigate('/');
                }
            } else {
                alert("Login failed. Please check your credentials.");
            }
        } catch (error) {
            console.error("Login error: ", error);
            alert("An error occurred during login. Please try again.");
            navigate('/login');
        }
    };

    const handlePasswordReset = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Open the pop up window
        setResetModal(true);
    }

    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            
            <form onSubmit={handleLogin} className="flex flex-col h-screen items-center justify-center">
                <h1 className="p-6 text-3xl font-bold text-[#CBDB2F]">Login</h1>
                <div className="flex flex-col items-start">
                    <label htmlFor="username" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Username</label>
                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Your username"
                        className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                    />
                </div>
                <div className="flex flex-col items-start">
                    <label htmlFor="password" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Password</label>
                    <input
                        id="password"
                        type="password"
                        placeholder="Your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                    />
                </div>
                <div className="flex justify-between items-center text-sm">
                    <div>
                        <input
                            type="checkbox"
                            id="remember"
                            onChange={(e) => setRemember(e.target.checked)}
                            className="-mr-1"
                        />
                        <label htmlFor="remember" className="m-2 text-[#CBDB2F]">Remember Me</label>
                    </div>    
                    <a className="m-2 text-[#CBDB2F] underline hover:text-white" href="#" onClick={handlePasswordReset}>Forgot Password</a>
                </div>
                <div className="m-2 sm:m-6">
                    <Button size={"xl"} type="submit">Sign In</Button>
                </div>
                <div className="flex text-xs sm:text-sm">
                    <p className="mr-1 text-[#CBDB2F]">Don't have an account?&nbsp;
                        <Link
                            to="/register"
                            className="text-[#CBDB2F] underline hover:text-white"
                        >
                            Register
                        </Link>
                    </p>
                </div>
            </form>
            {resetModal && (
                <PasswordResetModal onClose={() => setResetModal(false)} />
            )}
        </div>
    )
}

export default Login;