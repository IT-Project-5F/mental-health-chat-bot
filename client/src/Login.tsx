import { useNavigate, Link } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        navigate("/");
    };
    return (
        <div className="absolute w-screen h-screen bg-[#01563E] inset-0">
            <form onSubmit={handleLogin} className="flex flex-col h-screen items-center justify-center">
                <h1 className="p-2 sm:p-6 text-lg sm:text-3xl font-bold text-[#CBDB2F]">Login</h1>
                <div className="flex flex-col items-start">
                    <label htmlFor="email" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Email</label>
                    <input type="email" placeholder="Your email address" className="px-6 py-3 mb-2 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"/>
                </div>
                <div className="flex flex-col items-start">
                    <label htmlFor="password" className="m-2 text-[#CBDB2F] font-bold hidden sm:block">Password</label>
                    <input type="password" placeholder="Your password" className="px-6 py-3 mb-0 text-[#014532] font-bold placeholder-gray-600 placeholder:font-bold bg-white rounded-4xl border-5 border-[#01563E] focus:outline-none focus:ring-1 focus:ring-white transition duration-300 ease-in-out"/>
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