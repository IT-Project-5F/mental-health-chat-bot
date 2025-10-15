import { useNavigate, Link } from 'react-router-dom';
import { useState } from 'react';
import { request } from './api';
import { Button } from './components/ui/button';

function Register() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email_address, setEmailAddress] = useState("");
    const [location, setLocation] = useState("");

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        
        try {
            const result = await request("POST", "/api/auth/signup", { username, password, email_address, location }, true, "json");
            if (result && result.id) {
                localStorage.setItem("access_token", result.access_token);
                // Redirect to login page after registration and inform user to verify email
                alert("Thank you for registering! We will send you a confirmation email after we've verified your email.");
                navigate('/login');
            } else {
                alert("Registration failed.");
            }
        } catch (error) {
            console.error("Registration error: ", error);
            alert("An error occurred during registration. Please try again.");
            navigate('/register');
        }
    };

    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            <form onSubmit={handleRegister} className="flex flex-col h-screen items-center justify-center">
                <h1 className="p-6 text-3xl font-bold text-[#CBDB2F]">Register</h1>
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
                    <label htmlFor="email" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Email</label>
                    <input
                        id="email"
                        type="text"
                        placeholder="Your email"
                        value={email_address}
                        onChange={(e) => setEmailAddress(e.target.value)}
                        className="px-6 py-3 m-1 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"
                    />
                </div>
                <div className="flex flex-col items-start">
                    <label htmlFor="location" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Location</label>
                    <input
                        id="location"
                        type="text"
                        placeholder="Your location"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
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
                <div className="m-2 sm:m-6 text-sm sm:text-lg">
                    <Button size={"xl"} type="submit">Register</Button>
                </div>
                <div className="flex text-xs sm:text-sm">
                    <p className="mr-1 text-[#CBDB2F]">Already have an account?&nbsp;
                        <Link
                            to="/login"
                            className="text-[#CBDB2F] underline hover:text-white"
                        >
                            Log In
                        </Link>
                    </p>
                </div>
            </form>
        </div>
    )
}

export default Register;