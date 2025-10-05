import { useNavigate, Link } from 'react-router-dom';
import { request } from './api';
import { useState } from 'react';

function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("")

    // Example login function
    const handleLogin = async (e: React.FormEvent) => {
            e.preventDefault();

            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            
            // const response = await fetch("http://localhost:5001/api/auth/login", {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/x-www-form-urlencoded',
            //     },
            //     body: formData.toString(),
            // });

            const result = await request("POST", "/api/auth/login", { username, password }, true, "form");
            if (result.access_token) {
                localStorage.setItem("access_token", result.access_token);
                navigate('/admin');
            } else {
                navigate('/login');
            }
    };

    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            <form onSubmit={handleLogin} className="flex flex-col h-screen items-center justify-center">
                <h1 className="p-2 sm:p-6 text-lg sm:text-3xl font-bold text-[#CBDB2F]">Login</h1>
                <div className="flex flex-col items-start">
                    <label htmlFor="username" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Email</label>
                    <input
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
                        type="password"
                        placeholder="Your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="px-6 py-3 mb-0 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                    />
                </div>
                <div className="flex flex-wrap sm:flex-nowrap justify-between items-center text-sm">
                    <input type="checkbox" id="remember" className="-mr-1"/>
                    <label htmlFor="remember" className="m-2">Remember Me</label>
                    <a className="m-2" href="#">Forgot Password</a>
                </div>
                <div className="flex flex-col m-2 sm:m-6 text-sm sm:text-lg">
                    <button className="px-8 sm:px-10 py-2 m-2 font-bold text-[#014532] bg-[#CBDB2F] rounded-3xl hover:bg-[#62BB46] hover:scale-102 duration-150">Sign In</button>
                    {/*<button className="px-8 sm:px-10 py-2 m-2 font-bold text-[#014532] bg-[#CBDB2F] rounded-3xl hover:bg-[#62BB46] hover:scale-102 duration-150">Sign In with Google</button>
                    */}
                </div>
                <div className="flex text-xs sm:text-sm">
                    <p className="mr-1 text-[#CBDB2F]">Don't have an account?</p>
                    <Link
                        to="/register"
                    >
                        Register
                    </Link>
                </div>
            </form>
        </div>
    )
}

export default Login;