import { useNavigate, Link } from 'react-router-dom';
<<<<<<< HEAD
import { request } from './api';
import { useState } from 'react';
=======
import { useState } from 'react';
import { request } from './api';
>>>>>>> main

function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
<<<<<<< HEAD
    const [password, setPassword] = useState("")

    // Example login function
    const handleLogin = async (e: React.FormEvent) => {
            e.preventDefault();

            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const result = await request("POST", "/api/auth/login", { username, password }, true, "form");
            if (result.access_token) {
                localStorage.setItem("access_token", result.access_token);
                navigate('/admin');
            } else {
=======
    const [password, setPassword] = useState("");
    const [remember, setRemember] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
            e.preventDefault();

            try {
                const result = await request("POST", "/api/auth/login", { username, password }, true, "form");

                if (result && result.access_token) {
                    // Check if user selected "Remember"
                    if (remember) {
                        // Persist login
                        localStorage.setItem("access_token", result.access_token);
                    } else {
                        // Clears (signs out) when browser closes
                        sessionStorage.setItem("access_token", result.access_token);
                    }
                    navigate('/admin');
                } else {
                    alert("Login failed. Please check your credentials.");
                }
            } catch (error) {
                console.error("Login error: ", error);
                alert("An error occurred during login. Please try again.");
>>>>>>> main
                navigate('/login');
            }
    };

<<<<<<< HEAD
=======
    const handlePasswordReset = async (e: React.FormEvent) => {
        e.preventDefault();
        
        try {
            const result = await request("POST", `/api/auth/reset/${username}`, { username }, true, "json");
            if (result && result.message) {
                alert("Password reset link sent to your email.");
            }
        } catch (error) {
            console.error("Password reset error: ", error);
            alert("An error occurred during password reset. Please try again.");
            navigate('/login');
        }
    }

>>>>>>> main
    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            <form onSubmit={handleLogin} className="flex flex-col h-screen items-center justify-center">
                <h1 className="p-2 sm:p-6 text-lg sm:text-3xl font-bold text-[#CBDB2F]">Login</h1>
                <div className="flex flex-col items-start">
                    <label htmlFor="username" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Username</label>
                    <input
<<<<<<< HEAD
=======
                        id="username"
>>>>>>> main
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Your username"
                        className="px-6 py-3 mb-2 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                    />
                </div>
                <div className="flex flex-col items-start">
                    <label htmlFor="password" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Password</label>
                    <input
<<<<<<< HEAD
=======
                        id="password"
>>>>>>> main
                        type="password"
                        placeholder="Your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="px-6 py-3 mb-0 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
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
                <div className="flex flex-col m-2 sm:m-6 text-sm sm:text-lg">
                    <button className="px-8 sm:px-10 py-2 m-2 font-bold text-[#014532] bg-[#CBDB2F] rounded-3xl hover:bg-[#62BB46] hover:scale-102 duration-150">Sign In</button>
                </div>
                <div className="flex text-xs sm:text-sm">
                    <p className="mr-1 text-[#CBDB2F]">Don't have an account?</p>
                    <Link
                        to="/register"
                        className='text-[#CBDB2F] underline hover:text-white'
                    >
                        Register
                    </Link>
                </div>
            </form>
        </div>
    )
}

export default Login;